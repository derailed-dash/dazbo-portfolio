from fastapi import Request

from app.services.blog_service import BlogService
from app.services.experience_service import ExperienceService
from app.services.project_service import ProjectService
from app.services.session_service import FirestoreSessionService


def get_project_service(request: Request) -> ProjectService:
    return request.app.state.project_service


def get_blog_service(request: Request) -> BlogService:
    return request.app.state.blog_service


def get_experience_service(request: Request) -> ExperienceService:
    return request.app.state.experience_service


def get_session_service(request: Request) -> FirestoreSessionService:
    return request.app.state.session_service
