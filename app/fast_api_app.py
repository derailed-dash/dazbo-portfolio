"""
Description: FastAPI application entry point and configuration.
Why: Initializes the web server, middleware, routes, and application lifespan events.
How: Configures FastAPI with ADK integration, Telemetry, and Firestore services. Uses a lifespan context manager for startup/shutdown logic.
"""

import json
import logging
import os
from contextlib import asynccontextmanager

import anyio
import google.auth
from fastapi import Depends, FastAPI, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
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
)
from app.models.application import Application
from app.models.blog import Blog
from app.models.content import Content
from app.models.experience import Experience
from app.models.project import Project
from app.services.application_service import ApplicationService
from app.services.blog_service import BlogService
from app.services.content_service import ContentService
from app.services.experience_service import ExperienceService
from app.services.firestore import close_client, get_client
from app.services.project_service import ProjectService

# Suppress noisy OpenTelemetry attribute warnings
os.environ["OTEL_PYTHON_LOG_LEVEL"] = "ERROR"
# Also suppress the specific opentelemetry attributes logger if needed
logging.getLogger("opentelemetry.attributes").setLevel(logging.ERROR)

# Rate Limiter Initialization
limiter = Limiter(key_func=get_remote_address, headers_enabled=True)

_, project_id = google.auth.default()
logging_client = google_cloud_logging.Client()
logger = logging_client.logger(__name__)
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
        async for event in runner.run_async(
            new_message=msg,
            user_id=chat_request.user_id,
            session_id=session.id,
            run_config=RunConfig(streaming_mode=StreamingMode.SSE),
        ):
            logger.log_text(f"Received event: partial={getattr(event, 'partial', 'N/A')}, turn_complete={getattr(event, 'turn_complete', 'N/A')}", severity="DEBUG")

            # Log significant events for diagnostics
            if event.turn_complete:
                logger.log_text(f"Turn complete for session {session.id}", severity="INFO")

            # Check for function calls (tools being used)
            if hasattr(event, "content") and event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "function_call") and part.function_call:
                        logger.log_text(f"Agent calling tool: {part.function_call.name}", severity="INFO")

            # Extract text from the event (ModelResponse)
            # ADK yields partial=True for incremental chunks and partial=False for merged/final content.
            # To avoid duplication in the UI, we prioritize partial=True chunks.
            # If we've yielded ANY partial chunks, we ignore the final non-partial chunk.
            # If we HAVEN'T yielded any partial chunks, we yield the non-partial chunk (supports non-streaming models).

            text_chunk = ""
            try:
                parts = []
                if hasattr(event, "content") and event.content and event.content.parts:
                    parts = event.content.parts
                elif hasattr(event, "candidates") and event.candidates:
                    candidate = event.candidates[0]
                    if candidate.content and candidate.content.parts:
                        parts = candidate.content.parts

                # Only process text if parts exist
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
                logger.log_text(f"Error parsing event: {e}", severity="ERROR")

            if text_chunk:
                payload = {"content": text_chunk}
                yield f"data: {json.dumps(payload)}\n\n"

            # If it's the final event, notify the stream is closing
            if event.turn_complete:
                yield "data: [DONE]\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.post("/api/feedback")
def collect_feedback(feedback: Feedback) -> dict[str, str]:
    """Collect and log feedback."""
    logger.log_struct(feedback.model_dump(), severity="INFO")
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
if os.path.exists(frontend_dist):
    # Mount assets folder for images, css, js
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Check if a static file exists (e.g. favicon.ico, manifest.json)
        file_path = os.path.join(frontend_dist, full_path)
        if full_path and await anyio.to_thread.run_sync(os.path.isfile, file_path):
            return FileResponse(file_path)

        # Default to index.html for React Router (client-side routing)
        return FileResponse(os.path.join(frontend_dist, "index.html"))


# Main execution
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
