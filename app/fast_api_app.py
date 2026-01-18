"""
Description: FastAPI application entry point and configuration.
Why: Initializes the web server, middleware, routes, and application lifespan events.
How: Configures FastAPI with ADK integration, Telemetry, and Firestore services. Uses a lifespan context manager for startup/shutdown logic.
"""

import os
from contextlib import asynccontextmanager

import google.auth
from fastapi import Depends, FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from google.adk.cli.fast_api import get_fast_api_app
from google.adk.sessions import InMemorySessionService
from google.cloud import firestore
from google.cloud import logging as google_cloud_logging

from app.app_utils.telemetry import setup_telemetry
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
from app.services.project_service import ProjectService

setup_telemetry()
_, project_id = google.auth.default()
logging_client = google_cloud_logging.Client()
logger = logging_client.logger(__name__)
allow_origins = os.getenv("ALLOW_ORIGINS", "").split(",") if os.getenv("ALLOW_ORIGINS") else None

# Artifact bucket for ADK (created by Terraform, passed via env var)
logs_bucket_name = os.environ.get("LOGS_BUCKET_NAME")

AGENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# In-memory session configuration - no persistent storage
session_service_uri = None

artifact_service_uri = f"gs://{logs_bucket_name}" if logs_bucket_name else None


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize Firestore client
    db = firestore.AsyncClient(project=settings.google_cloud_project, database=settings.firestore_database_id)
    app.state.firestore_db = db

    # Initialize Services
    app.state.project_service = ProjectService(db)
    app.state.blog_service = BlogService(db)
    app.state.experience_service = ExperienceService(db)
    app.state.session_service = InMemorySessionService()

    yield
    # Clean up
    db.close()


app: FastAPI = get_fast_api_app(
    agents_dir=AGENT_DIR,
    web=False,
    artifact_service_uri=artifact_service_uri,
    allow_origins=allow_origins,
    session_service_uri=session_service_uri,
    otel_to_cloud=True,
    lifespan=lifespan,
)
app.title = "dazbo-portfolio"
app.description = "API for interacting with the Agent dazbo-portfolio"


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
    async def serve_react_app(full_path: str):
        """Catch-all route to serve the React SPA."""
        # Check if the requested path is a specific file in the dist folder (e.g. favicon.ico)
        file_path = os.path.join(frontend_dist, full_path)
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)

        # Default to index.html for React Router (client-side routing)
        return FileResponse(os.path.join(frontend_dist, "index.html"))


# Main execution
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
