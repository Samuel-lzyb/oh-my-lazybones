"""Skill request/response schemas."""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class SkillCreate(BaseModel):
    """Payload for creating a skill."""

    name: str = Field(
        ...,
        pattern=r"^[a-z0-9-]{3,64}$",
        examples=["daily-email-digest"],
    )
    version: str = Field(default="0.1.0", pattern=r"^\d+\.\d+\.\d+$")
    author: str = Field(..., min_length=1, max_length=64)
    description: str = Field(default="", max_length=2000)
    tags: List[str] = Field(default=[], max_length=10)
    depends_on: List[str] = Field(default=[], max_length=20)
    actions: List[dict] = Field(default=[], max_length=50)


class SkillResponse(BaseModel):
    """Skill returned by the API."""

    id: str
    name: str
    version: str
    author: str
    description: str
    tags: List[str]
    downloads: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SkillSearchParams(BaseModel):
    """Query parameters for skill search."""

    q: Optional[str] = Field(None, description="Search keyword")
    tag: Optional[str] = Field(None, description="Filter by tag")
    sort: str = Field("downloads", pattern=r"^(downloads|created_at)$")
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)
