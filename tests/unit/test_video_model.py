"""
Description: Unit tests for the Video model.
Why: Ensures the Video model correctly validates its fields and handles defaults.
How: Uses pytest and Pydantic validation.
"""

import pytest
from pydantic import ValidationError

from app.models.video import Video


def test_video_model_valid():
    """Test valid video data."""
    data = {
        "title": "Test Video",
        "description": "A test video description.",
        "thumbnail_url": "https://example.com/thumb.jpg",
        "publish_date": "2024-03-24",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "is_manual": True,
        "source_platform": "youtube",
    }
    video = Video(**data)
    assert video.title == "Test Video"
    assert video.is_manual is True
    assert video.source_platform == "youtube"


def test_video_model_missing_fields():
    """Test validation error for missing required fields."""
    data = {"title": "Test Video"}
    with pytest.raises(ValidationError):
        Video(**data)


def test_video_model_defaults():
    """Test default values for the video model."""
    data = {
        "title": "Test Video",
        "description": "A test video description.",
        "video_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    }
    video = Video(**data)
    assert video.is_manual is True
    assert video.source_platform == "youtube"
    assert video.thumbnail_url is None
