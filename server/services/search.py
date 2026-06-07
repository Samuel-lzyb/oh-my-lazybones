"""Search service — abstract + Meilisearch implementation."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

from meilisearch import Client

INDEX_NAME = "skills"


class SearchService(ABC):
    """Abstract search backend. M2 uses Meilisearch; M3 can swap."""

    @abstractmethod
    async def index(self, skill: Dict[str, Any]) -> None: ...

    @abstractmethod
    async def deindex(self, name: str) -> None: ...

    @abstractmethod
    async def search(
        self, query: str, tag: str | None,
        sort: str, page: int, limit: int,
    ) -> tuple[List[str], int]: ...

    @abstractmethod
    async def reindex_all(self, skills: List[Dict[str, Any]]) -> None: ...


class MeilisearchService(SearchService):
    """Meilisearch-backed search."""

    def __init__(self, url: str, master_key: str):
        self.client = Client(url, master_key)

    @staticmethod
    def _skill_to_doc(skill: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a skill dict to a Meilisearch document."""
        return {
            "id": skill["name"],
            "name": skill["name"],
            "version": skill.get("version", ""),
            "author": skill.get("author", ""),
            "description": skill.get("description", ""),
            "tags": skill.get("tags", []),
            "downloads": skill.get("downloads", 0),
            "created_at": str(skill.get("created_at", "")),
        }

    async def ensure_index(self) -> None:
        """Idempotent: create or update the skills index."""
        self.client.index(INDEX_NAME).update_settings({
            "searchableAttributes": ["name", "description", "tags", "author"],
            "filterableAttributes": ["tags"],
            "sortableAttributes": ["downloads", "created_at"],
        })

    async def index(self, skill: Dict[str, Any]) -> None:
        doc = self._skill_to_doc(skill)
        self.client.index(INDEX_NAME).add_documents([doc])

    async def deindex(self, name: str) -> None:
        self.client.index(INDEX_NAME).delete_document(name)

    async def search(
        self, query: str, tag: str | None,
        sort: str, page: int, limit: int,
    ) -> tuple[List[str], int]:
        params: Dict[str, Any] = {
            "limit": limit,
            "offset": (page - 1) * limit,
            "sort": [f"{sort}:desc"],
        }
        if tag:
            params["filter"] = f'tags = "{tag}"'

        result = self.client.index(INDEX_NAME).search(query, params)
        names = [hit["id"] for hit in result["hits"]]
        total = result.get("estimatedTotalHits", 0)
        return names, total

    async def reindex_all(self, skills: List[Dict[str, Any]]) -> None:
        docs = [self._skill_to_doc(s) for s in skills]
        if docs:
            self.client.index(INDEX_NAME).add_documents(docs)


class SQLiteSearchService(SearchService):
    """SQLite LIKE-based search — no external dependencies."""

    def __init__(self, db_url: str):
        self.db_url = db_url

    async def ensure_index(self) -> None:
        pass  # SQLite doesn't need index setup

    async def index(self, skill: Dict[str, Any]) -> None:
        pass  # SQLite stores skill in main table, no reindex needed

    async def deindex(self, name: str) -> None:
        pass

    async def search(
        self, query: str, tag: str | None,
        sort: str, page: int, limit: int,
    ) -> tuple[List[str], int]:
        """Search via SQL LIKE on the skills table."""
        from sqlalchemy import select, func, or_
        from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
        from ..models.skill import Skill

        engine = create_async_engine(self.db_url, echo=False)
        session_factory = async_sessionmaker(engine, expire_on_commit=False)

        async with session_factory() as session:
            stmt = select(Skill)
            if query:
                pattern = f"%{query}%"
                stmt = stmt.where(
                    or_(
                        Skill.name.like(pattern),
                        Skill.description.like(pattern),
                        Skill.author.like(pattern),
                    )
                )
            if tag:
                stmt = stmt.where(Skill.tags.contains([tag]))

            # Count
            count_stmt = select(func.count()).select_from(stmt.subquery())
            total = (await session.execute(count_stmt)).scalar() or 0

            # Sort and paginate
            sort_col = Skill.downloads if sort == "downloads" else Skill.created_at
            stmt = stmt.order_by(sort_col.desc()).offset((page - 1) * limit).limit(limit)
            result = await session.execute(stmt)
            skills = list(result.scalars().all())

        await engine.dispose()
        return [s.name for s in skills], total

    async def reindex_all(self, skills: List[Dict[str, Any]]) -> None:
        pass  # Not needed for SQLite
