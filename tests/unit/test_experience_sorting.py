"""
Description: Unit tests for Experience sorting.
Why: Ensures experience entries are retrieved in reverse chronological order.
How: Mocks Firestore client and verifies `order_by` is called on the collection query.
"""

import pytest
from unittest.mock import MagicMock
from google.cloud import firestore
from app.services.experience_service import ExperienceService

@pytest.mark.asyncio
async def test_experience_service_list_sorts_by_start_date_descending():
    mock_db = MagicMock(spec=firestore.AsyncClient)
    mock_collection = MagicMock()
    mock_query = MagicMock()
    
    mock_db.collection.return_value = mock_collection
    mock_collection.order_by.return_value = mock_query
    
    async def mock_stream():
        if False: yield None
    
    mock_collection.stream.return_value = mock_stream()
    mock_query.stream.return_value = mock_stream()
    
    service = ExperienceService(mock_db)
    await service.list()
    
    mock_collection.order_by.assert_called_with("start_date", direction=firestore.Query.DESCENDING)
