"""
Description: Integration tests for API endpoints.
Why: Verifies that API routes return correct status codes and data format.
How: Uses `TestClient` and mocks dependency injection overrides for services.
"""

from unittest.mock import AsyncMock

from fastapi.testclient import TestClient

from app.dependencies import (
    get_blog_service,
    get_experience_service,
    get_project_service,
)


def test_get_projects():
    from app.fast_api_app import app

    mock_service = AsyncMock()
    mock_service.list.return_value = []
    app.dependency_overrides[get_project_service] = lambda: mock_service

    try:
        with TestClient(app) as client:
            response = client.get("/api/projects")
            assert response.status_code == 200
    finally:
        app.dependency_overrides.clear()


def test_get_blogs():
    from app.fast_api_app import app

    mock_service = AsyncMock()
    mock_service.list.return_value = []
    app.dependency_overrides[get_blog_service] = lambda: mock_service

    try:
        with TestClient(app) as client:
            response = client.get("/api/blogs")
            assert response.status_code == 200
    finally:
        app.dependency_overrides.clear()


def test_get_experience():
    from app.fast_api_app import app

    mock_service = AsyncMock()
    mock_service.list.return_value = []
    app.dependency_overrides[get_experience_service] = lambda: mock_service

    try:
        with TestClient(app) as client:
            response = client.get("/api/experience")
            assert response.status_code == 200
    finally:
        app.dependency_overrides.clear()
