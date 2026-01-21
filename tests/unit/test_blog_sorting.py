"""
Description: Unit tests for Blog sorting.
Why: Ensures blogs are retrieved in reverse chronological order.
How: Mocks Firestore client and verifies `order_by` is called on the collection query.
"""

from unittest.mock import MagicMock

import pytest
from google.cloud import firestore

from app.services.blog_service import BlogService


@pytest.mark.asyncio
async def test_blog_service_list_sorts_by_date_descending():
    mock_db = MagicMock(spec=firestore.AsyncClient)
    mock_collection = MagicMock()
    mock_query = MagicMock()

    mock_db.collection.return_value = mock_collection

    # Setup chain: collection.order_by(...).stream()
    mock_collection.order_by.return_value = mock_query

    # Mock stream to yield nothing
    async def mock_stream():
        if False:
            yield None

    # If the code calls collection.stream() directly (failing case), we need to handle that too
    mock_collection.stream.return_value = mock_stream()
    mock_query.stream.return_value = mock_stream()

    service = BlogService(mock_db)
    await service.list()

    # Verify order_by was called with 'date', DESCENDING
    # This should FAIL with current implementation
    mock_collection.order_by.assert_called_with("date", direction=firestore.Query.DESCENDING)
