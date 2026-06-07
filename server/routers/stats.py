"""Stats endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..repositories.skill import SkillRepository

router = APIRouter(prefix="/api/v1", tags=["stats"])


@router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    """Get platform statistics."""
    repo = SkillRepository(db)
    return {
        "skills": await repo.count(),
        "authors": await repo.count_distinct_authors(),
        "installs": await repo.sum_downloads(),
    }
