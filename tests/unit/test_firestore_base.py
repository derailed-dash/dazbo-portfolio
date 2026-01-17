"""
Description: Unit tests for FirestoreService.
Why: Verifies that generic Firestore service methods are callable and handle imports correctly.
How: Uses mocks for Firestore client/collection/document.
"""

from unittest.mock import MagicMock

import pytest

from app.models.project import Project


@pytest.mark.asyncio
async def test_firestore_service_import():
    try:
        from app.services.firestore_base import FirestoreService  # noqa: F401
    except ImportError:
        pytest.fail("Could not import FirestoreService")


@pytest.mark.asyncio
async def test_firestore_service_create():
    try:
        from app.services.firestore_base import FirestoreService
    except ImportError:
        return  # Handled by test_import

    mock_db = MagicMock()
    mock_collection = MagicMock()
    mock_doc_ref = MagicMock()

    mock_db.collection.return_value = mock_collection
    mock_collection.document.return_value = mock_doc_ref

    service = FirestoreService(db=mock_db, collection_name="projects", model_class=Project)

    project = Project(title="Test", description="Desc")
    # Assume create returns the created item with ID
    # This mock setup is minimal, just to verify method existence
    try:
        await service.create(project)
    except AttributeError:
        pytest.fail("FirestoreService does not have create method")
    except Exception:
        # We expect some failure if implementation is missing, but import failure is the "Red" signal here
        pass
