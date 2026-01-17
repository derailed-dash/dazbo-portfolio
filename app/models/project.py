from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class Project(BaseModel):
    id: Optional[str] = None
    title: str
    description: str
    tags: List[str] = Field(default_factory=list)
    repo_url: Optional[str] = None
    demo_url: Optional[str] = None
    image_url: Optional[str] = None
    featured: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
