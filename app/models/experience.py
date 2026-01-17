from typing import List, Optional
from pydantic import BaseModel, Field

class Experience(BaseModel):
    id: Optional[str] = None
    company: str
    role: str
    duration: str
    description: str
    skills: List[str] = Field(default_factory=list)
    order: int = 0
