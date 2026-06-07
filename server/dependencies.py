"""FastAPI dependency injection — wires up the dependency chain."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings
from .database import get_db
from .repositories.skill import SkillRepository
from .services.search import MeilisearchService, SQLiteSearchService, SearchService
from .services.skill_registry import SkillRegistry

_search_service: SearchService | None = None


def get_search_service() -> SearchService:
    """Auto-detect search backend: Meilisearch if available, else SQLite."""
    global _search_service
    if _search_service is None:
        meili_url = settings.meili_url
        if meili_url and meili_url.startswith("http"):
            try:
                _search_service = MeilisearchService(meili_url, settings.meili_master_key)
            except Exception:
                _search_service = SQLiteSearchService(settings.database_url)
        else:
            _search_service = SQLiteSearchService(settings.database_url)
    return _search_service


async def get_skill_registry(
    db: AsyncSession = Depends(get_db),
    search: SearchService = Depends(get_search_service),
) -> SkillRegistry:
    """Assemble SkillRegistry with its dependencies."""
    repo = SkillRepository(db)
    return SkillRegistry(repo, search)
