from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from pydantic import BaseModel

from app.services.blog_service import BlogService
from app.services.firestore_base import FirestoreService
from app.services.project_service import ProjectService


class SitemapTestModel(BaseModel):
    id: str | None = None
    title: str
    date: str


@pytest.mark.asyncio
async def test_list_projection():
    # Setup
    mock_db = AsyncMock()
    mock_db.collection = MagicMock()
    mock_collection = MagicMock()
    mock_db.collection.return_value = mock_collection

    # Mock query chain
    mock_query = MagicMock()
    mock_collection.select.return_value = mock_query
    mock_query.order_by.return_value = mock_query

    # Mock stream results
    mock_doc1 = MagicMock()
    mock_doc1.id = "doc1"
    mock_doc1.to_dict.return_value = {"title": "Title 1", "date": "2023-01-01"}

    mock_doc2 = MagicMock()
    mock_doc2.id = "doc2"
    mock_doc2.to_dict.return_value = {"title": "Title 2", "date": "2023-01-02"}

    # Configure stream to return an async iterator
    async def async_stream():
        yield mock_doc1
        yield mock_doc2

    mock_query.stream.return_value = async_stream()

    # Instantiate service
    service = FirestoreService(mock_db, "test_collection", SitemapTestModel)

    # Execute
    fields = ["title", "date"]
    results = await service.list_projection(fields, order_by="date")

    # Verify
    mock_collection.select.assert_called_with(fields)
    mock_query.order_by.assert_called_with("date", direction="DESCENDING")

    assert len(results) == 2
    assert results[0] == {"id": "doc1", "title": "Title 1", "date": "2023-01-01"}
    assert results[1] == {"id": "doc2", "title": "Title 2", "date": "2023-01-02"}


@pytest.mark.asyncio
async def test_blog_sitemap_entries():
    mock_db = AsyncMock()
    # db.collection() is synchronous, so it should be a MagicMock, not AsyncMock
    mock_db.collection = MagicMock()
    service = BlogService(mock_db)

    # Mock list_projection
    service.list_projection = AsyncMock(
        return_value=[
            {"id": "b1", "date": "2023-01-01", "is_private": False},
            {"id": "b2", "date": "2023-01-02", "is_private": True},
            {"id": "b3", "date": "2023-01-03", "is_private": False},
        ]
    )

    entries = await service.get_sitemap_entries()

    service.list_projection.assert_called_with(["date", "is_private"], order_by="date")
    assert len(entries) == 2
    assert entries[0]["id"] == "b1"
    assert entries[1]["id"] == "b3"


@pytest.mark.asyncio
async def test_project_sitemap_entries():
    mock_db = AsyncMock()
    # db.collection() is synchronous
    mock_db.collection = MagicMock()
    service = ProjectService(mock_db)

    dt = datetime(2023, 1, 1, 12, 0, 0)

    # Mock list_projection
    service.list_projection = AsyncMock(return_value=[{"id": "p1", "created_at": dt}, {"id": "p2", "created_at": None}])

    entries = await service.get_sitemap_entries()

    service.list_projection.assert_called_with(["created_at"], order_by="created_at")
    assert len(entries) == 2
    assert entries[0]["id"] == "p1"
    assert entries[0]["lastmod"] == dt.isoformat()
    assert entries[1]["lastmod"] is None
