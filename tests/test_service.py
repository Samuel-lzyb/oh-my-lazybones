"""Service layer tests."""

import pytest
from fastapi import HTTPException

from server.schemas.skill import SkillCreate, SkillSearchParams


@pytest.mark.asyncio
class TestSkillRegistry:
    async def test_create_success(self, registry):
        data = SkillCreate(name="svc-test", author="dev", tags=["api"])
        skill = await registry.create(data)
        assert skill.name == "svc-test"
        assert skill.id is not None

    async def test_create_duplicate(self, registry):
        data = SkillCreate(name="svc-dup", author="dev")
        await registry.create(data)
        with pytest.raises(HTTPException) as exc:
            await registry.create(data)
        assert exc.value.status_code == 409

    async def test_get_by_name_found(self, registry):
        data = SkillCreate(name="svc-get", author="dev")
        await registry.create(data)
        skill = await registry.get_by_name("svc-get")
        assert skill.name == "svc-get"

    async def test_get_by_name_not_found(self, registry):
        with pytest.raises(HTTPException) as exc:
            await registry.get_by_name("nonexistent")
        assert exc.value.status_code == 404

    async def test_search_with_query(self, registry, search_svc):
        data = SkillCreate(name="email-digest", author="dev", description="email tool")
        await registry.create(data)

        params = SkillSearchParams(q="email")
        skills, total = await registry.search(params)
        assert total == 1
        assert skills[0].name == "email-digest"

    async def test_search_no_results(self, registry):
        params = SkillSearchParams(q="nothing")
        skills, total = await registry.search(params)
        assert total == 0

    async def test_delete_success(self, registry):
        data = SkillCreate(name="svc-del", author="dev")
        await registry.create(data)
        await registry.delete("svc-del")
        with pytest.raises(HTTPException) as exc:
            await registry.get_by_name("svc-del")
        assert exc.value.status_code == 404
