"""Skill-specific repository."""

from typing import Optional

from sqlalchemy import select
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
        skill = await self.get_by_name(name)
        if skill:
            skill.downloads += 1
            await self.session.commit()
