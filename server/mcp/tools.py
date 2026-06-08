"""MCP tool implementations — thin wrappers around existing services.

Uses direct service instantiation (not FastAPI Depends) because
MCP SSE tools run outside FastAPI's request context.
"""

from mcp.server.fastmcp import FastMCP
from sqlalchemy.ext.asyncio import async_sessionmaker

from ..database import engine
from ..dependencies import get_search_service
from ..exceptions import SkillConflictError, SkillNotFoundError
from ..repositories.skill import SkillRepository
from ..schemas.skill import SkillCreate, SkillSearchParams
from ..services.skill_registry import SkillRegistry


def _skill_to_dict(skill) -> dict:
    """Serialize a Skill ORM object to dict for MCP tool responses."""
    return {
        "name": skill.name,
        "version": skill.version,
        "author": skill.author,
        "description": skill.description,
        "tags": skill.tags or [],
        "downloads": skill.downloads or 0,
    }


async def _make_registry() -> SkillRegistry:
    """Create a SkillRegistry with its own short-lived DB session."""
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    async with session_factory() as db:
        repo = SkillRepository(db)
        search = get_search_service()
        return SkillRegistry(repo, search)


def register_tools(mcp: FastMCP) -> None:
    """Register all MCP tools on the given FastMCP instance."""

    # ── Discovery ──

    @mcp.tool()
    async def search_skills(
        query: str,
        tags: list[str] | None = None,
        limit: int = 10,
    ) -> list[dict]:
        """Search for Agent Skills by keyword. Returns matching skills with metadata."""
        registry = await _make_registry()
        params = SkillSearchParams(
            q=query,
            tag=tags[0] if tags else None,
            sort="downloads",
            limit=limit,
        )
        results, _total = await registry.search(params)
        return [_skill_to_dict(s) for s in results]

    @mcp.tool()
    async def get_skill(name: str) -> dict:
        """Get full details of a single Skill by name."""
        registry = await _make_registry()
        try:
            skill = await registry.get_by_name(name)
        except Exception:
            raise SkillNotFoundError(name)
        return _skill_to_dict(skill)

    @mcp.tool()
    async def list_categories() -> dict:
        """List all available Skill categories (tags) across the marketplace."""
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

    # ── Lifecycle ──

    @mcp.tool()
    async def install_skill(name: str) -> dict:
        """Install a Skill by name. Returns skill metadata on success."""
        registry = await _make_registry()
        try:
            skill = await registry.get_by_name(name)
        except Exception:
            raise SkillNotFoundError(name)
        return {"action": "installed", **_skill_to_dict(skill)}

    @mcp.tool()
    async def remove_skill(name: str) -> dict:
        """Remove/uninstall a Skill by name. Returns confirmation."""
        registry = await _make_registry()
        try:
            await registry.delete(name)
        except Exception:
            raise SkillNotFoundError(name)
        return {"action": "removed", "name": name}

    @mcp.tool()
    async def publish_skill(
        name: str,
        version: str = "0.1.0",
        author: str = "",
        description: str = "",
        tags: list[str] | None = None,
    ) -> dict:
        """Publish a new Skill to the marketplace.

        Args:
            name: Skill name (lowercase, hyphens, 3-64 chars)
            version: Semver version string (default "0.1.0")
            author: Author identifier
            description: Short description of what the Skill does
            tags: Optional list of category tags
        """
        registry = await _make_registry()
        data = SkillCreate(
            name=name,
            version=version,
            author=author,
            description=description,
            tags=tags or [],
        )
        try:
            skill = await registry.create(data)
        except Exception:
            raise SkillConflictError(name)
        return {"action": "published", **_skill_to_dict(skill)}
