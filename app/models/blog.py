from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class Blog(BaseModel):
    id: Optional[str] = None
    title: str
    summary: str
    date: str # ISO 8601 string as per spec
    platform: str
    url: str
    created_at: datetime = Field(default_factory=datetime.now)
