from pydantic import BaseModel, Field


class Experience(BaseModel):
    id: str | None = None
    company: str
    role: str
    duration: str
    description: str
    skills: list[str] = Field(default_factory=list)
    order: int = 0
