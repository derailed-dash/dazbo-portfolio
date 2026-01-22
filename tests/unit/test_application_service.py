"""
Description: Unit tests for Application Service.
Why: Verifies that the ApplicationService correctly interacts with Firestore using the "applications" collection.
How: Mocks the Firestore AsyncClient and asserts on its calls.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services.application_service import ApplicationService
from app.models.application import Application

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.mark.asyncio
async def test_application_service_collection(mock_db):
    mock_db.collection.return_value.id = "applications"
    service = ApplicationService(mock_db)
    assert service.collection.id == "applications"
    assert service.model_class == Application

@pytest.mark.asyncio
async def test_list_applications(mock_db):
    service = ApplicationService(mock_db)
    
    # Mock Firestore stream
    mock_doc = MagicMock()
    mock_doc.to_dict.return_value = {
        "title": "Test App",
        "description": "Test Desc",
        "demo_url": "https://test.com",
        "tags": ["tag"],
        "is_manual": True,
        "source_platform": "application",
        "metadata_only": False
    }
    mock_doc.id = "test-app"
    
    mock_docs = AsyncMock()
    mock_docs.__aiter__.return_value = [mock_doc]
    mock_db.collection.return_value.stream.return_value = mock_docs
    
    apps = await service.list()
    
    assert len(apps) == 1
    assert apps[0].title == "Test App"
    mock_db.collection.assert_called_with("applications")
