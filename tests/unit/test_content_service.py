"""
Description: Unit tests for Content Service.
Why: Verifies that the ContentService correctly interacts with Firestore using the "content" collection.
How: Mocks the Firestore AsyncClient and asserts on its calls.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.mark.asyncio
async def test_content_service_init(mock_db):
    try:
        from app.models.content import Content
        from app.services.content_service import ContentService
    except ImportError:
        pytest.fail("Could not import ContentService or Content model")

    service = ContentService(mock_db)
    
    # We can't easily check the collection ID without calling a method that uses it,
    # or inspecting the init if it sets a public property.
    # The base class `FirestoreService` usually sets `self.collection`.
    # Let's assume we can access it or verify via a method call.
    
    assert service.model_class == Content


@pytest.mark.asyncio
async def test_get_content_by_slug(mock_db):
    try:
        from app.services.content_service import ContentService
    except ImportError:
        pytest.fail("Could not import ContentService")

    service = ContentService(mock_db)

    # Mock Firestore get
    mock_doc_ref = MagicMock()
    mock_doc_snapshot = MagicMock()
    mock_doc_snapshot.exists = True
    mock_doc_snapshot.to_dict.return_value = {
        "title": "About Me",
        "body": "# About Me",
        "last_updated": "2026-01-24T12:00:00Z"
    }
    mock_doc_snapshot.id = "about"
    
    mock_doc_ref.get = AsyncMock(return_value=mock_doc_snapshot)
    mock_db.collection.return_value.document.return_value = mock_doc_ref

    content = await service.get("about")

    assert content is not None
    assert content.title == "About Me"
    assert content.id == "about"
    mock_db.collection.assert_called_with("content")
    mock_db.collection.return_value.document.assert_called_with("about")
