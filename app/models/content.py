"""
Description: Content model for singleton pages.
Why: Represents generic content pages like 'About Me' in Firestore.
How: Uses Pydantic for validation.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Content(BaseModel):
    """
    Represents a generic content page.
    """

    id: Optional[str] = Field(None, description="The document ID (slug)")
    title: str = Field(..., description="The title of the page")
    body: str = Field(..., description="The markdown body content")
    last_updated: datetime = Field(..., description="Last updated timestamp")
