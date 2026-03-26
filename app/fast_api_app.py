"""
Description: FastAPI application entry point and configuration.
Why: Initializes the web server, middleware, routes, and application lifespan events.
How: Configures FastAPI with ADK integration, Telemetry, and Firestore services for content.
Note: Chat sessions are ephemeral and stored in-memory (not persisted to Firestore).
"""

import html
import json
import logging
import os
from contextlib import asynccontextmanager

import anyio
import google.auth
from fastapi import Depends, FastAPI, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.cli.fast_api import get_fast_api_app
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.cloud import logging as google_cloud_logging
from google.genai import types
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from app.agent import app as adk_app
from app.app_utils.typing import Feedback
from app.config import settings
from app.dependencies import (
    get_application_service,
    get_blog_service,
    get_content_service,
    get_experience_service,
    get_project_service,
    get_video_service,
)
from app.models.application import Application
from app.models.blog import Blog
from app.models.content import Content
from app.models.experience import Experience
from app.models.project import Project
from app.models.video import Video
from app.services.application_service import ApplicationService
from app.services.blog_service import BlogService
from app.services.content_service import ContentService
from app.services.experience_service import ExperienceService
from app.services.firestore import close_client, get_client
from app.services.project_service import ProjectService
from app.services.video_service import VideoService

# Suppress noisy OpenTelemetry attribute warnings
os.environ["OTEL_PYTHON_LOG_LEVEL"] = "ERROR"
# Also suppress the specific opentelemetry attributes logger if needed
logging.getLogger("opentelemetry.attributes").setLevel(logging.ERROR)

# Rate Limiter Initialization
limiter = Limiter(key_func=get_remote_address, headers_enabled=True)

# Cloud Logging initialization
try:
    if not os.getenv("K_SERVICE"):  # Not in Cloud Run
        raise Exception("Local environment")
    _, project_id = google.auth.default()
    logging_client = google_cloud_logging.Client()
    # This automatically captures standard logging and sends to Cloud Logging
    logging_client.setup_logging()
    logger = logging.getLogger(__name__)
except Exception:
    # Fallback to standard logging if not in GCP or local
    logging.basicConfig(
        level=getattr(logging, settings.log_level), format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger = logging.getLogger(__name__)
    # Ensure all app loggers follow this
    logging.getLogger("app").setLevel(getattr(logging, settings.log_level))
    cloud_logger = None
allow_origins = os.getenv("ALLOW_ORIGINS", "").split(",") if os.getenv("ALLOW_ORIGINS") else None

AGENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# In-memory session configuration - no persistent storage
session_service_uri = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Firestore client
    db = get_client()
    app.state.firestore_db = db

    # Initialize Services
    app.state.project_service = ProjectService(db)
    app.state.application_service = ApplicationService(db)
    app.state.blog_service = BlogService(db)
    app.state.content_service = ContentService(db)
    app.state.experience_service = ExperienceService(db)
    app.state.video_service = VideoService(db)
    app.state.session_service = InMemorySessionService()

    yield
    # Clean up
    close_client()


app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=False,
    allow_origins=allow_origins,
    session_service_uri=session_service_uri,
    otel_to_cloud=False,
    lifespan=lifespan,
)
app.title = "dazbo-portfolio"
app.description = "API for interacting with the Agent dazbo-portfolio"

SITE_TITLE = 'Darren "Dazbo" Lester - Enterprise Cloud Architect and Google Evangelist'

# Add Limiter to app state and exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)


class ChatRequest(BaseModel):
    user_id: str
    message: str


@app.post("/api/chat/stream")
@limiter.limit("5/minute")
async def chat_stream(request: Request, chat_request: ChatRequest):
    """
    Streaming chat endpoint for the portfolio agent.
    """
    session_service = app.state.session_service

    # Get or create a session for the user
    sessions = await session_service.list_sessions(user_id=chat_request.user_id, app_name=settings.app_name)
    if sessions.sessions:
        session = sessions.sessions[0]
    else:
        session = await session_service.create_session(user_id=chat_request.user_id, app_name=settings.app_name)

    runner = Runner(app=adk_app, session_service=session_service)

    msg = types.Content(
        role="user",
        parts=[types.Part.from_text(text=f"<user_query>{chat_request.message}</user_query>")],
    )

    async def event_generator():
        yielded_partial = False
        try:
            async for event in runner.run_async(
                new_message=msg,
                user_id=chat_request.user_id,
                session_id=session.id,
                run_config=RunConfig(streaming_mode=StreamingMode.SSE),
            ):
                # logger.debug(f"Agent event: {type(event).__name__} (turn_complete={getattr(event, 'turn_complete', 'N/A')})")

                text_chunk = ""
                try:
                    parts = []
                    # Standard ModelResponse handling
                    if hasattr(event, "content") and event.content and getattr(event.content, "parts", None):
                        parts = event.content.parts

                    if parts:
                        is_partial = getattr(event, "partial", False)

                        # Yield text if it's a partial chunk OR if we haven't yielded any partials yet.
                        if is_partial or not yielded_partial:
                            current_text_parts = [p.text for p in parts if hasattr(p, "text") and p.text]
                            if current_text_parts:
                                text_chunk = "".join(current_text_parts)
                                if is_partial:
                                    yielded_partial = True

                except Exception as e:
                    logger.error(f"Error parsing event: {e}")

                if text_chunk:
                    # In SSE streaming mode, ADK might send the full accumulated text in each event
                    # or just the delta. We need to handle this based on what the frontend expects.
                    # For now, we assume delta or handle accumulation in the frontend.
                    payload = {"content": text_chunk}
                    yield f"data: {json.dumps(payload)}\n\n"

                # If it's the final event, notify the stream is closing
                if getattr(event, "turn_complete", False):
                    yield "data: [DONE]\n\n"
        except Exception as e:
            logger.error(f"Critical error in event generator: {e}", exc_info=True)
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
            yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.post("/api/feedback")
def collect_feedback(feedback: Feedback) -> dict[str, str]:
    """Collect and log feedback."""
    logger.debug(f"Feedback received: {feedback.model_dump()}")
    return {"status": "success"}


@app.get("/api/projects", response_model=list[Project])
@limiter.limit("60/minute")
async def list_projects(request: Request, service: ProjectService = Depends(get_project_service)):
    """List all projects."""
    data = await service.list()
    return JSONResponse(content=jsonable_encoder(data))


@app.get("/api/applications", response_model=list[Application])
@limiter.limit("60/minute")
async def list_applications(request: Request, service: ApplicationService = Depends(get_application_service)):
    """List all curated applications."""
    data = await service.list()
    return JSONResponse(content=jsonable_encoder(data))


@app.get("/api/blogs", response_model=list[Blog])
@limiter.limit("60/minute")
async def list_blogs(request: Request, service: BlogService = Depends(get_blog_service)):
    """List all blog posts."""
    data = await service.list()
    return JSONResponse(content=jsonable_encoder(data))


@app.get("/api/videos", response_model=list[Video])
@limiter.limit("60/minute")
async def list_videos(request: Request, service: VideoService = Depends(get_video_service)):
    """List all YouTube videos."""
    data = await service.list()
    return JSONResponse(content=jsonable_encoder(data))


@app.get("/api/experience", response_model=list[Experience])
@limiter.limit("60/minute")
async def list_experience(request: Request, service: ExperienceService = Depends(get_experience_service)):
    """List all work experience."""
    data = await service.list()
    return JSONResponse(content=jsonable_encoder(data))


@app.get("/api/content/{slug}", response_model=Content)
@limiter.limit("60/minute")
async def get_content(slug: str, request: Request, service: ContentService = Depends(get_content_service)):
    """Retrieve a content page by slug."""
    doc = await service.get(slug)
    if not doc:
        return JSONResponse(status_code=404, content={"message": "Content not found"})
    return JSONResponse(content=jsonable_encoder(doc))


@app.get("/sitemap.xml")
@limiter.limit("10/minute")
async def sitemap_xml(request: Request):
    """Generate XML sitemap."""
    import xml.etree.ElementTree as ET

    base_url = settings.base_url.rstrip("/") if settings.base_url else str(request.base_url).rstrip("/")

    if not settings.base_url:
        logger.log_text(
            "BASE_URL environment variable not set. Using request URL as base for sitemap. This may be incorrect if the application is behind a reverse proxy. Set BASE_URL for production environments.",
            severity="WARNING",
        )

    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    def add_url(loc: str, lastmod: str | None = None, changefreq: str = "monthly", priority: str = "0.7"):
        url = ET.SubElement(urlset, "url")
        # Ensure loc starts with base_url if it's not already absolute
        full_url = loc if loc.startswith("http") else f"{base_url}{loc}"
        ET.SubElement(url, "loc").text = full_url
        if lastmod:
            ET.SubElement(url, "lastmod").text = lastmod
        ET.SubElement(url, "changefreq").text = changefreq
        ET.SubElement(url, "priority").text = priority

    # Static pages
    add_url("/", changefreq="daily", priority="1.0")
    add_url("/about", changefreq="monthly", priority="0.8")

    xml_content = f'<?xml version="1.0" encoding="UTF-8"?>\n{ET.tostring(urlset, encoding="unicode")}'

    return Response(content=xml_content, media_type="application/xml")


# --- Static File Serving (Unified Origin) ---

# Mount static files if they exist (production/container mode)
frontend_dist = os.path.join(AGENT_DIR, "frontend", "dist")
assets_dir = os.path.join(frontend_dist, "assets")
if os.path.exists(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")


def _generate_head_tags(title: str, description: str, path: str, base_url: str, json_ld: dict | None = None) -> str:
    default_image = f"{base_url}/images/dazbo-profile.png"
    # Ensure path starts with /
    normalized_path = f"/{path.lstrip('/')}"
    url = f"{base_url}{normalized_path}" if normalized_path != "/" else f"{base_url}/"
    full_title = title if title == SITE_TITLE else f"{title} | {SITE_TITLE}"

    esc_title = html.escape(full_title, quote=True)
    esc_desc = html.escape(description, quote=True)
    esc_url = html.escape(url, quote=True)
    esc_image = html.escape(default_image, quote=True)

    # Base tags
    tags = [
        f"<title>{esc_title}</title>",
        f'<meta name="description" content="{esc_desc}" />',
        f'<link rel="canonical" href="{esc_url}" />',
    ]

    # Open Graph
    tags.extend(
        [
            f'<meta property="og:title" content="{esc_title}" />',
            f'<meta property="og:description" content="{esc_desc}" />',
            '<meta property="og:type" content="website" />',
            f'<meta property="og:url" content="{esc_url}" />',
            f'<meta property="og:image" content="{esc_image}" />',
        ]
    )

    # Twitter tags intentionally omitted as per user request

    if json_ld:
        # We do not HTML escape JSON-LD; we dump it safely into the script tag.
        # However, we must ensure that no </script> tags reside within the JSON.
        json_str = json.dumps(json_ld).replace("</script>", "<\\/script>")
        tags.append(f'<script type="application/ld+json">\n{json_str}\n</script>')

    return "".join(tags)


def _get_seo_data_dict(path: str, base_url: str) -> dict:
    seo_map = {
        "/": {
            "title": SITE_TITLE,
            "description": 'The professional portfolio of Darren "Dazbo" Lester: Enterprise Cloud Architect, Google Cloud Evangelist, AI Champion and Google Developer Expert (GDE).',
            "json_ld": {
                "@context": "https://schema.org",
                "@type": "Person",
                "@id": "https://darrenlester.net/#person",
                "name": "Darren Lester",
                "alternateName": "Dazbo",
                "jobTitle": "Enterprise Cloud Architect",
                "url": base_url,
                "sameAs": [
                    "https://github.com/derailed-dash",
                    "https://www.linkedin.com/in/darren-lester-architect/",
                    "https://medium.com/@derailed.dash",
                    "https://dev.to/deraileddash",
                    "https://sessionize.com/dazbo/",
                ],
                "knowsAbout": [
                    "Google Cloud",
                    "Generative AI",
                    "Model Context Protocol",
                    "Architecture",
                    "ADK",
                    "Agentic AI",
                    "Gemini",
                    "Gemini CLI",
                ],
                "description": "Enterprise Cloud Architect, Google Developer Expert (GDE), and Google AI Champion, specializing in Google Cloud, agentic AI, cloud architecture and cloud strategy. Note: Not to be confused with the frontend engineer or other individuals of the same name.",
            },
        },
        "/about": {
            "title": "About Darren Lester",
            "description": 'Learn more about Darren "Dazbo" Lester, his background, skills and achievements.',
        },
    }

    seo_data = seo_map.get(
        path,
        {
            "title": path.lstrip("/").replace("-", " ").title(),
            "description": f"View {path.lstrip('/').replace('-', ' ')} on Darren Lester's portfolio.",
        },
    )

    head_tags = _generate_head_tags(seo_data["title"], seo_data["description"], path, base_url, seo_data.get("json_ld"))

    full_title = seo_data["title"] if seo_data["title"] == SITE_TITLE else f"{seo_data['title']} | {SITE_TITLE}"
    return {"head_tags": head_tags, "title": full_title}


@app.get("/api/seo")
@limiter.limit("60/minute")
async def get_seo_data(request: Request, path: str = "/"):
    """Return SEO title and description for a given path."""
    base_url = settings.base_url or str(request.base_url).rstrip("/")
    return JSONResponse(content=_get_seo_data_dict(path, base_url))


@app.get("/{full_path:path}")
async def serve_spa(request: Request, full_path: str):
    # Security: Prevent path traversal
    # Resolve the absolute path of the requested file
    actual_frontend_dist = os.path.abspath(frontend_dist)
    requested_path = os.path.abspath(os.path.join(actual_frontend_dist, full_path))

    # Check if the requested path is within the frontend_dist directory
    if not requested_path.startswith(actual_frontend_dist):
        return JSONResponse(status_code=403, content={"message": "Forbidden"})

    # Check if a static file exists (e.g. favicon.ico, manifest.json)
    if full_path and await anyio.to_thread.run_sync(os.path.isfile, requested_path):
        return FileResponse(requested_path)

    # It's a route, serve index.html with SEO injection
    index_path = os.path.join(actual_frontend_dist, "index.html")
    if not await anyio.to_thread.run_sync(os.path.isfile, index_path):
        return JSONResponse(status_code=404, content={"message": "Frontend not built"})

    with open(index_path, encoding="utf-8") as f:
        html = f.read()

    # Inject SEO tags for known routes
    path = f"/{full_path}" if full_path else "/"
    base_url = settings.base_url or str(request.base_url).rstrip("/")
    seo_data = _get_seo_data_dict(path, base_url)
    head_tags = seo_data.get("head_tags")

    if head_tags:
        html = html.replace("<!-- __SEO_TAGS__ -->", head_tags)

    return HTMLResponse(content=html)


# Main execution
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
