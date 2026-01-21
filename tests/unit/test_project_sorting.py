"""
Description: Unit tests for Project sorting.
Why: Ensures projects are retrieved in reverse chronological order.
How: Mocks Firestore client and verifies `order_by` is called on the collection query.
"""

import pytest
from unittest.mock import MagicMock
from google.cloud import firestore
from app.services.project_service import ProjectService

@pytest.mark.asyncio
async def test_project_service_list_sorts_by_created_at_descending():
    mock_db = MagicMock(spec=firestore.AsyncClient)
    mock_collection = MagicMock()
    mock_query = MagicMock()
    
    mock_db.collection.return_value = mock_collection
    mock_collection.order_by.return_value = mock_query
    
    async def mock_stream():
        if False: yield None
    
    mock_collection.stream.return_value = mock_stream()
    mock_query.stream.return_value = mock_stream()
    
    service = ProjectService(mock_db)
    await service.list()
    
    mock_collection.order_by.assert_called_with("created_at", direction=firestore.Query.DESCENDING)
