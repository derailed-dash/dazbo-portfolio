"""
Description: FastAPI dependency injection providers.
Why: Decouples route handlers from service instantiation and ensures consistent access to shared resources.
How: Provides functions to retrieve services (ProjectService, BlogService, etc.) from `request.app.state`.
"""

from fastapi import Request

from app.services.application_service import ApplicationService
from app.services.blog_service import BlogService
from app.services.content_service import ContentService
from app.services.experience_service import ExperienceService
from app.services.project_service import ProjectService
from app.services.session_service import FirestoreSessionService


def get_project_service(request: Request) -> ProjectService:
    return request.app.state.project_service


def get_application_service(request: Request) -> ApplicationService:
    return request.app.state.application_service


def get_blog_service(request: Request) -> BlogService:
    return request.app.state.blog_service


def get_content_service(request: Request) -> ContentService:
    return request.app.state.content_service


def get_experience_service(request: Request) -> ExperienceService:
    return request.app.state.experience_service


def get_session_service(request: Request) -> FirestoreSessionService:
    return request.app.state.session_service
