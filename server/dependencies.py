"""FastAPI dependency injection — wires up the dependency chain."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings
from .database import get_db
from .repositories.skill import SkillRepository
from .services.search import MeilisearchService
from .services.skill_registry import SkillRegistry

_search_service: MeilisearchService | None = None


def get_search_service() -> MeilisearchService:
    """Singleton Meilisearch client, created once per process."""
    global _search_service
    if _search_service is None:
        _search_service = MeilisearchService(
            settings.meili_url, settings.meili_master_key
        )
    return _search_service


async def get_skill_registry(
    db: AsyncSession = Depends(get_db),
    search: MeilisearchService = Depends(get_search_service),
) -> SkillRegistry:
    """Assemble SkillRegistry with its dependencies."""
    repo = SkillRepository(db)
    return SkillRegistry(repo, search)
