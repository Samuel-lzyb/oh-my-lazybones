"""MCP tool implementations — thin wrappers around existing services.

Uses direct service instantiation (not FastAPI Depends) because
MCP SSE tools run outside FastAPI's request context.
"""

from fastapi import HTTPException
from mcp.server.fastmcp import FastMCP
from sqlalchemy.ext.asyncio import async_sessionmaker

from ..config import settings
from ..database import engine
from ..repositories.skill import SkillRepository
from ..schemas.skill import SkillSearchParams
from ..services.search import MeilisearchService, SQLiteSearchService, SearchService
from ..services.skill_registry import SkillRegistry

_search_service: SearchService | None = None


def _get_search_service() -> SearchService:
    global _search_service
    if _search_service is None:
        meili_url = settings.meili_url
        if meili_url and meili_url.startswith("http"):
            try:
                _search_service = MeilisearchService(
                    meili_url, settings.meili_master_key
                )
            except Exception:
                _search_service = SQLiteSearchService(settings.database_url)
        else:
            _search_service = SQLiteSearchService(settings.database_url)
    return _search_service


async def _make_registry() -> SkillRegistry:
    """Create a SkillRegistry with its own DB session."""
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    db = session_factory()
    repo = SkillRepository(db)
    search = _get_search_service()
    return SkillRegistry(repo, search)


def register_tools(mcp: FastMCP) -> None:
    """Register all MCP tools on the given FastMCP instance."""

    @mcp.tool()
    async def search_skills(
        query: str,
        tags: list[str] | None = None,
        limit: int = 10,
    ) -> list[dict]:
        """Search for Agent Skills by keyword."""
        registry = await _make_registry()
        params = SkillSearchParams(
            q=query,
            tag=tags[0] if tags else None,
            sort="downloads",
            limit=limit,
        )
        results, _total = await registry.search(params)
        return [
            {
                "name": s.name,
                "version": s.version,
                "author": s.author,
                "description": s.description,
                "tags": s.tags or [],
                "downloads": s.downloads or 0,
            }
            for s in results
        ]

    @mcp.tool()
    async def install_skill(name: str) -> dict:
        """Install a Skill by name."""
        registry = await _make_registry()
        try:
            skill = await registry.get_by_name(name)
        except HTTPException:
            return {"status": "error", "message": f"Skill '{name}' not found"}

        return {
            "status": "installed",
            "name": skill.name,
            "version": skill.version,
            "author": skill.author,
            "description": skill.description,
            "tags": skill.tags or [],
        }

    @mcp.tool()
    async def list_categories() -> dict:
        """List all available Skill categories (tags)."""
        registry = await _make_registry()
        params = SkillSearchParams(
            q=None, tag=None, sort="downloads", limit=100
        )
        results, _total = await registry.search(params)

        tags_set: set[str] = set()
        for s in results:
            for t in (s.tags or []):
                tags_set.add(t)

        return {"categories": sorted(tags_set)}
