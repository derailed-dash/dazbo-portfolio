"""
Description: Integration tests for rate limiting.
Why: Verifies that global and specific rate limits are enforced.
How: Uses `TestClient` to simulate repeated requests and check for 429 status.
"""

from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from app.dependencies import get_project_service
from app.fast_api_app import app

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
