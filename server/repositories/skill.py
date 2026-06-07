"""Skill-specific repository."""

from typing import Optional

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.skill import Skill
from .base import AbstractRepository


class SkillRepository(AbstractRepository[Skill]):
    """CRUD + lookup operations for Skill."""

    model = Skill

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_name(self, name: str) -> Optional[Skill]:
        result = await self.session.execute(
            select(Skill).where(Skill.name == name)
        )
        return result.scalar_one_or_none()

    async def increment_downloads(self, name: str) -> None:
        await self.session.execute(
            update(Skill)
            .where(Skill.name == name)
            .values(downloads=Skill.downloads + 1)
        )
        await self.session.commit()

    async def count_distinct_authors(self) -> int:
        result = await self.session.execute(
            select(func.count(func.distinct(Skill.author)))
        )
        return result.scalar() or 0

    async def sum_downloads(self) -> int:
        result = await self.session.execute(select(func.sum(Skill.downloads)))
        return result.scalar() or 0
