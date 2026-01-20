"""
Description: Integration tests for rate limiting.
Why: Verifies that global and specific rate limits are enforced.
How: Uses `TestClient` to simulate repeated requests and check for 429 status.
"""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_project_service
from app.fast_api_app import app, limiter


@pytest.fixture(autouse=True)
def reset_limiter():
    """Reset the limiter storage before each test."""
    limiter.reset()


def test_global_rate_limit():
    """
    Test that the global rate limit (60/minute) is enforced.
    """
    # Mock the service to avoid DB hits
    mock_service = AsyncMock()
    mock_service.list.return_value = []
    app.dependency_overrides[get_project_service] = lambda: mock_service

    try:
        with TestClient(app) as client:
            # First 60 requests should succeed
            for _ in range(60):
                response = client.get("/api/projects")
                assert response.status_code == 200

            # The 61st request should fail with 429
            response = client.get("/api/projects")
            assert response.status_code == 429
            assert "Rate limit exceeded" in response.text
    finally:
        app.dependency_overrides.clear()


@patch("app.services.firestore.get_client")
def test_chat_rate_limit(mock_get_client):
    """
    Test that the chat endpoint rate limit (5/minute) is enforced.
    """
    # Use a mock payload
    payload = {"user_id": "test_user", "message": "Hello"}

    # Mock the firestore client to return a mock
    mock_db = AsyncMock()
    mock_get_client.return_value = mock_db

    # Mock services to avoid DB hits from tools
    mock_proj_service = AsyncMock()
    mock_proj_service.list.return_value = []
    mock_blog_service = AsyncMock()
    mock_blog_service.list.return_value = []

    from app.dependencies import get_blog_service, get_project_service

    app.dependency_overrides[get_project_service] = lambda: mock_proj_service
    app.dependency_overrides[get_blog_service] = lambda: mock_blog_service

    try:
        with TestClient(app) as client:
            # First 5 requests should succeed (or at least not be 429)
            for _ in range(5):
                response = client.post("/api/chat/stream", json=payload)
                assert response.status_code != 429

            # The 6th request should fail with 429
            response = client.post("/api/chat/stream", json=payload)
            assert response.status_code == 429
            assert "Rate limit exceeded" in response.text
    finally:
        app.dependency_overrides.clear()
