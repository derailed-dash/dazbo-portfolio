"""
Description: Blog data model.
Why: Defines the schema for blog posts stored in Firestore and returned by the API.
How: Uses Pydantic BaseModel to define fields like title, summary, date, url, etc.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class Blog(BaseModel):
    id: str | None = None
    title: str
    summary: str | None = None
    date: str  # ISO 8601 string as per spec
    platform: str
    url: str
    source_platform: str | None = None
    is_manual: bool = True
    metadata_only: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
