"""Repository tests — real SQLite."""

import pytest

from server.models.skill import Skill


@pytest.mark.asyncio
class TestSkillRepository:
    async def test_create(self, repo):
        skill = Skill(name="r-test", version="0.1.0", author="dev")
        created = await repo.create(skill)
        assert created.id is not None
        assert created.name == "r-test"
        assert created.created_at is not None

    async def test_get_by_name_exists(self, repo, sample_skill):
        found = await repo.get_by_name("test-skill")
        assert found is not None
        assert found.name == "test-skill"

    async def test_get_by_name_not_found(self, repo):
        found = await repo.get_by_name("nonexistent")
        assert found is None

    async def test_list_all(self, repo, sample_skill):
        skills = await repo.list_all(0, 20)
        assert len(skills) >= 1

    async def test_list_all_pagination(self, repo, sample_skill):
        skills = await repo.list_all(0, 1)
        assert len(skills) == 1

    async def test_count(self, repo, sample_skill):
        assert await repo.count() >= 1

    async def test_delete(self, repo, sample_skill):
        await repo.delete(sample_skill)
        found = await repo.get_by_name("test-skill")
        assert found is None

    async def test_increment_downloads(self, repo, sample_skill):
        before = sample_skill.downloads
        await repo.increment_downloads("test-skill")
        # Re-fetch to verify
        skill = await repo.get_by_name("test-skill")
        assert skill.downloads == before + 1

    async def test_count_distinct_authors(self, repo, sample_skill):
        count = await repo.count_distinct_authors()
        assert count >= 1

    async def test_sum_downloads(self, repo, sample_skill):
        total = await repo.sum_downloads()
        assert total >= 0
