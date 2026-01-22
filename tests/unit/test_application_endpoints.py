"""
Description: Unit tests for Application API endpoints.
Why: Verifies that the /api/applications endpoint returns the correct data.
How: Uses FastAPI TestClient and dependency overrides to mock the ApplicationService.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock

from app.fast_api_app import app
from app.dependencies import get_application_service
from app.models.application import Application

client = TestClient(app)

@pytest.fixture
def mock_application_service():
    service = AsyncMock()
    app.dependency_overrides[get_application_service] = lambda: service
    yield service
    app.dependency_overrides.clear()

def test_get_applications(mock_application_service):
    # Mock data
    mock_apps = [
        Application(
            id="app-1",
            title="App 1",
            description="Desc 1",
            demo_url="https://demo1.com",
            tags=["tag1"],
            is_manual=True,
            source_platform="application",
            metadata_only=False
        )
    ]
    mock_application_service.list.return_value = mock_apps

    response = client.get("/api/applications")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "App 1"
    assert data[0]["source_platform"] == "application"
