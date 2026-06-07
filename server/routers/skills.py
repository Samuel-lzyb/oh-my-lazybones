"""Skill API endpoints."""

from fastapi import APIRouter, Depends, Query

from ..dependencies import get_skill_registry
from ..schemas.common import PaginatedResponse
from ..schemas.skill import (
    SkillCreate,
    SkillResponse,
    SkillSearchParams,
)
from ..services.skill_registry import SkillRegistry

router = APIRouter(prefix="/api/v1/skills", tags=["skills"])


@router.post("", status_code=201, response_model=SkillResponse)
async def create_skill(
    data: SkillCreate,
    registry: SkillRegistry = Depends(get_skill_registry),
):
    """Register a new skill."""
    return await registry.create(data)


@router.get("", response_model=PaginatedResponse[SkillResponse])
async def search_skills(
    q: str | None = Query(None, description="Search keyword"),
    tag: str | None = Query(None, description="Filter by tag"),
    sort: str = Query("downloads", pattern=r"^(downloads|created_at)$"),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    registry: SkillRegistry = Depends(get_skill_registry),
):
    """Search or list skills."""
    params = SkillSearchParams(q=q, tag=tag, sort=sort, page=page, limit=limit)
    skills, total = await registry.search(params)
    return PaginatedResponse(items=skills, total=total, page=page, limit=limit)


@router.get("/{name}", response_model=SkillResponse)
async def get_skill(
    name: str,
    registry: SkillRegistry = Depends(get_skill_registry),
):
    """Get a skill by name."""
    return await registry.get_by_name(name)


@router.delete("/{name}", status_code=204)
async def delete_skill(
    name: str,
    registry: SkillRegistry = Depends(get_skill_registry),
):
    """Delete a skill."""
    await registry.delete(name)
