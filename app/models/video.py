"""
Description: Video data model.
Why: Defines the schema for YouTube videos in the portfolio.
How: Uses Pydantic for validation and serialization.
"""


from pydantic import BaseModel, Field


class Video(BaseModel):
    """
    Represents a YouTube video entry.
    """
    id: str | None = Field(None, description="Firestore document ID")
    title: str = Field(..., description="The title of the video")
    description: str = Field(..., description="A description of the video content")
    thumbnail_url: str | None = Field(None, description="URL to the video thumbnail image")
    publish_date: str | None = Field(None, description="The date the video was published (ISO 8601 format)")
    video_url: str = Field(..., description="The direct URL to the YouTube video")
    is_manual: bool = Field(True, description="Indicates if the video was added manually")
    source_platform: str = Field("youtube", description="The source platform of the video (e.g., youtube)")
