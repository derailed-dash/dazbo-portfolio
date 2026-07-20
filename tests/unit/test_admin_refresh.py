"""
Description: Unit tests for the admin refresh endpoint.
Why: Verifies that the /api/admin/refresh endpoint works correctly, handles authentication bypass in dev, enforces the concurrency guard, and kicks off background tasks.
How: Uses FastAPI TestClient and mock objects to isolate the ingestion runner.
"""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.fast_api_app import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_settings():
    # Store old values
    old_github = settings.github_user
    old_project = settings.google_cloud_project
    old_log_level = settings.log_level

    # Set mock values
    settings.github_user = "test-github-user"
    settings.google_cloud_project = ""  # Local environment bypasses OIDC
    settings.log_level = "DEBUG"

    # Reset concurrency guard
    app.state.is_ingesting = False

    yield

    # Restore old values
    settings.github_user = old_github
    settings.google_cloud_project = old_project
    settings.log_level = old_log_level
    app.state.is_ingesting = False


@patch("app.tools.ingest.ingest_resources", new_callable=AsyncMock)
def test_trigger_refresh_success(mock_ingest):
    """Test that a successful call schedules background ingestion and returns 200."""
    response = client.post("/api/admin/refresh")

    assert response.status_code == 200
    assert response.json() == {"status": "refresh triggered"}


@patch("app.tools.ingest.ingest_resources", new_callable=AsyncMock)
def test_trigger_refresh_concurrency_guard(mock_ingest):
    """Test that when ingestion is already running, it returns 409 Conflict."""
    app.state.is_ingesting = True

    response = client.post("/api/admin/refresh")

    assert response.status_code == 409
    assert "already in progress" in response.json()["detail"]


@patch("app.tools.ingest.ingest_resources", new_callable=AsyncMock)
def test_trigger_refresh_missing_github_user(mock_ingest):
    """Test that it returns 400 if github_user is not configured."""
    settings.github_user = ""

    response = client.post("/api/admin/refresh")

    assert response.status_code == 400
    assert "github_user is not configured" in response.json()["detail"]


@patch("google.oauth2.id_token.verify_oauth2_token")
@patch("app.tools.ingest.ingest_resources", new_callable=AsyncMock)
def test_trigger_refresh_oidc_success(mock_ingest, mock_verify):
    """Test successful OIDC token validation and verification of audience."""
    settings.google_cloud_project = "dazbo-portfolio"
    settings.log_level = "INFO"
    mock_verify.return_value = {"email": "dazbo-portfolio-scheduler@dazbo-portfolio.iam.gserviceaccount.com"}

    response = client.post(
        "/api/admin/refresh",
        headers={"Authorization": "Bearer valid-fake-token"}
    )

    assert response.status_code == 200
    assert response.json() == {"status": "refresh triggered"}
    mock_verify.assert_called_once()
    # Check that it verified the expected audience URL
    _, kwargs = mock_verify.call_args
    assert kwargs.get("audience") == "http://testserver/api/admin/refresh"


def test_trigger_refresh_oidc_missing_header():
    """Test that a missing Authorization header returns 401."""
    settings.google_cloud_project = "dazbo-portfolio"
    settings.log_level = "INFO"

    response = client.post("/api/admin/refresh")

    assert response.status_code == 401
    assert "Missing or invalid Authorization header" in response.json()["detail"]


@patch("google.oauth2.id_token.verify_oauth2_token")
def test_trigger_refresh_oidc_unauthorized_email(mock_verify):
    """Test that an unauthorized caller email returns 403."""
    settings.google_cloud_project = "dazbo-portfolio"
    settings.log_level = "INFO"
    mock_verify.return_value = {"email": "attacker@evil.com"}

    response = client.post(
        "/api/admin/refresh",
        headers={"Authorization": "Bearer valid-fake-token"}
    )

    assert response.status_code == 403
    assert "Forbidden" in response.json()["detail"]

