"""Skill business logic — orchestrates Repository + SearchService."""

from typing import List, Tuple

from fastapi import HTTPException, status

from ..models.skill import Skill
from ..repositories.skill import SkillRepository
from ..schemas.skill import SkillCreate, SkillSearchParams
from .search import SearchService


class SkillRegistry:
    """Business logic for skill CRUD + search."""

    def __init__(self, repo: SkillRepository, search_svc: SearchService):
        self.repo = repo
        self._search = search_svc

    async def create(self, data: SkillCreate) -> Skill:
        existing = await self.repo.get_by_name(data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "CONFLICT",
                    "message": f"Skill '{data.name}' already exists",
                },
            )

        skill = Skill(
            name=data.name,
            version=data.version,
            author=data.author,
            description=data.description,
            tags=data.tags,
        )
        skill = await self.repo.create(skill)

        # Sync to Meilisearch (best-effort)
        try:
            await self._search.index(skill.to_dict())
        except Exception:
            pass

        return skill

    async def search(
        self, params: SkillSearchParams
    ) -> Tuple[List[Skill], int]:
        if params.q or params.tag:
            return await self._search_with_meili(params)
        return await self._list_from_db(params)

    async def _search_with_meili(
        self, params: SkillSearchParams
    ) -> Tuple[List[Skill], int]:
        names, total = await self._search.search(
            params.q or "", params.tag,
            params.sort, params.page, params.limit,
        )
        skills = []
        for name in names:
            s = await self.repo.get_by_name(name)
            if s:
                skills.append(s)
        return skills, total

    async def _list_from_db(
        self, params: SkillSearchParams
    ) -> Tuple[List[Skill], int]:
        offset = (params.page - 1) * params.limit
        skills = await self.repo.list_all(offset, params.limit)
        total = await self.repo.count()
        return skills, total

    async def get_by_name(self, name: str) -> Skill:
        skill = await self.repo.get_by_name(name)
        if not skill:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "NOT_FOUND",
                    "message": f"Skill '{name}' not found",
                },
            )
        return skill

    async def delete(self, name: str) -> None:
        skill = await self.get_by_name(name)
        await self.repo.delete(skill)
        try:
            await self._search.deindex(name)
        except Exception:
            pass

    async def suggest(self, name: str, limit: int = 3) -> list[str]:
        """Find skills with similar names via fuzzy matching."""
        from ..exceptions import suggest_name

        skills = await self.repo.list_all(0, 100)
        return suggest_name(name, [s.name for s in skills], limit)
