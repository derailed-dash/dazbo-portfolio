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
from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.adk.cli.fast_api import get_fast_api_app
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.cloud import logging as google_cloud_logging
from google.genai import types
from pydantic import BaseModel

from app.agent import app as adk_app
from app.app_utils.typing import Feedback
from app.config import settings
from app.dependencies import (
    get_blog_service,
    get_experience_service,
    get_project_service,
)
from app.models.blog import Blog
from app.models.experience import Experience
from app.models.project import Project
from app.services.blog_service import BlogService
from app.services.experience_service import ExperienceService
from app.services.firestore import close_client, get_client
from app.services.project_service import ProjectService

# Suppress noisy OpenTelemetry attribute warnings
os.environ["OTEL_PYTHON_LOG_LEVEL"] = "ERROR"
# Also suppress the specific opentelemetry attributes logger if needed
logging.getLogger("opentelemetry.attributes").setLevel(logging.ERROR)

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
    app.state.blog_service = BlogService(db)
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


class ChatRequest(BaseModel):
    user_id: str
    message: str


@app.post("/api/chat/stream")
async def chat_stream(request: ChatRequest):
    """
    Streaming chat endpoint for the portfolio agent.
    """
    session_service = app.state.session_service

    # Get or create a session for the user
    sessions = await session_service.list_sessions(user_id=request.user_id, app_name=settings.app_name)
    if sessions.sessions:
        session = sessions.sessions[0]
    else:
        session = await session_service.create_session(user_id=request.user_id, app_name=settings.app_name)

    runner = Runner(app=adk_app, session_service=session_service)

    msg = types.Content(
        role="user",
        parts=[types.Part.from_text(text=f"<user_query>{request.message}</user_query>")],
    )

    async def event_generator():
        async for event in runner.run_async(
            new_message=msg,
            user_id=request.user_id,
            session_id=session.id,
            run_config=RunConfig(streaming_mode=StreamingMode.SSE),
        ):
            # ADK may yield a final non-partial event containing the full response.
            # We only want deltas (partial=True) to avoid duplication.
            if not getattr(event, "partial", False):
                continue

            # Extract text from the event (ModelResponse)
            text_chunk = ""
            try:
                # Check for direct content (ADK/GenAI flat structure)
                parts = []
                if hasattr(event, "content") and event.content and event.content.parts:
                    parts = event.content.parts
                # Fallback for candidates structure
                elif hasattr(event, "candidates") and event.candidates:
                    candidate = event.candidates[0]
                    if candidate.content and candidate.content.parts:
                        parts = candidate.content.parts

                for part in parts:
                    if hasattr(part, "text") and part.text:
                        text_chunk += part.text
            except Exception as e:
                logger.log_text(f"Error parsing event: {e}", severity="ERROR")

            if text_chunk:
                payload = {"content": text_chunk}
                yield f"data: {json.dumps(payload)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.post("/api/feedback")
def collect_feedback(feedback: Feedback) -> dict[str, str]:
    """Collect and log feedback."""
    logger.log_struct(feedback.model_dump(), severity="INFO")
    return {"status": "success"}


@app.get("/api/projects", response_model=list[Project])
async def list_projects(service: ProjectService = Depends(get_project_service)):
    """List all projects."""
    return await service.list()


@app.get("/api/blogs", response_model=list[Blog])
async def list_blogs(service: BlogService = Depends(get_blog_service)):
    """List all blog posts."""
    return await service.list()


@app.get("/api/experience", response_model=list[Experience])
async def list_experience(service: ExperienceService = Depends(get_experience_service)):
    """List all work experience."""
    return await service.list()


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
