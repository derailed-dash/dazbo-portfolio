"""
Description: Project data model.
Why: Defines the schema for portfolio projects.
How: Uses Pydantic BaseModel for fields like title, description, tags, urls.
Dependencies: pydantic.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class Project(BaseModel):
    id: str | None = None
    title: str
    description: str
    tags: list[str] = Field(default_factory=list)
    repo_url: str | None = None
    demo_url: str | None = None
    image_url: str | None = None
    featured: bool = False
    source_platform: str | None = None
    is_manual: bool = True
    metadata_only: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
