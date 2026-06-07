"""Stats endpoint."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.skill import Skill
from ..repositories.skill import SkillRepository

router = APIRouter(prefix="/api/v1", tags=["stats"])


@router.get("/stats")
async def get_stats(db: AsyncSession = Depends(get_db)):
    """Get platform statistics."""
    repo = SkillRepository(db)
    total_skills = await repo.count()

    # Count unique authors
    from sqlalchemy import func, select
    result = await db.execute(select(func.count(func.distinct(Skill.author))))
    total_authors = result.scalar() or 0

    # Total downloads
    result2 = await db.execute(select(func.sum(Skill.downloads)))
    total_installs = result2.scalar() or 0

    return {
        "skills": total_skills,
        "authors": total_authors,
        "installs": total_installs,
    }
