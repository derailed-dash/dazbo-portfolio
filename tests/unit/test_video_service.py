"""
Description: Unit tests for VideoService.
Why: Ensures VideoService correctly interacts with Firestore using the Video model.
How: Mocks Firestore AsyncClient and verifies CRUD operations.
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

from app.services.video_service import VideoService


@pytest.fixture
def mock_db():
    return MagicMock()


@pytest.fixture
def video_service(mock_db):
    return VideoService(mock_db)


@pytest.mark.asyncio
async def test_video_service_list(video_service, mock_db):
    """Test listing videos."""
    mock_doc = MagicMock()
    mock_doc.id = "youtube:test-video"
    mock_doc.to_dict.return_value = {
        "title": "Test Video",
        "description": "Desc",
        "video_url": "https://youtube.com/watch?v=123",
    }

    mock_stream = AsyncMock()
    mock_stream.__aiter__.return_value = [mock_doc]
    mock_db.collection.return_value.stream.return_value = mock_stream

    videos = await video_service.list()
    assert len(videos) == 1
    assert videos[0].title == "Test Video"
    assert videos[0].id == "youtube:test-video"
    mock_db.collection.assert_called_with("videos")
