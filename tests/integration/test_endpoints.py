"""
Description: Integration tests for API endpoints.
Why: Verifies that API routes return correct status codes and data format.
How: Uses `TestClient` and mocks dependency injection overrides for services.
"""

from unittest.mock import AsyncMock, MagicMock

from fastapi.testclient import TestClient

from app.dependencies import (
    get_blog_service,
    get_content_service,
    get_experience_service,
    get_project_service,
)


def test_get_projects():
    from app.fast_api_app import app

    mock_service = MagicMock()
    mock_service.list = AsyncMock(return_value=[])
    app.dependency_overrides[get_project_service] = lambda: mock_service

    try:
        with TestClient(app) as client:
            response = client.get("/api/projects")
            assert response.status_code == 200
    finally:
        app.dependency_overrides.clear()


def test_get_blogs():
    from app.fast_api_app import app

    mock_service = MagicMock()
    mock_service.list = AsyncMock(return_value=[])
    app.dependency_overrides[get_blog_service] = lambda: mock_service

    try:
        with TestClient(app) as client:
            response = client.get("/api/blogs")
            assert response.status_code == 200
    finally:
        app.dependency_overrides.clear()


def test_get_experience():
    from app.fast_api_app import app

    mock_service = MagicMock()
    mock_service.list = AsyncMock(return_value=[])
    app.dependency_overrides[get_experience_service] = lambda: mock_service

    try:
        with TestClient(app) as client:
            response = client.get("/api/experience")
            assert response.status_code == 200
    finally:
        app.dependency_overrides.clear()


def test_get_content():
    from app.fast_api_app import app
    from app.models.content import Content
    from datetime import UTC, datetime

    mock_service = MagicMock()
    mock_content = Content(
        id="about",
        title="About Me",
        body="Test Body",
        last_updated=datetime.now(UTC),
    )
    mock_service.get = AsyncMock(return_value=mock_content)
    app.dependency_overrides[get_content_service] = lambda: mock_service

    try:
        with TestClient(app) as client:
            response = client.get("/api/content/about")
            assert response.status_code == 200
            assert response.json()["title"] == "About Me"
    finally:
        app.dependency_overrides.clear()
