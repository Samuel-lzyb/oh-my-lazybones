"""Tests for Tap system — Phase 3 stubs."""

from pathlib import Path

import pytest

from server.tap import TapInfo, TapRegistry, TapSkill


class TestTapInfo:
    def test_user_repo_parsing(self):
        info = TapInfo(name="samuel-lzyb/agent-skills", url="https://github.com/samuel-lzyb/agent-skills", path=Path("/tmp"))
        assert info.user == "samuel-lzyb"
        assert info.repo == "agent-skills"

    def test_enabled_default(self):
        info = TapInfo(name="test/repo", url="https://example.com", path=Path("/tmp"))
        assert info.enabled is True


class TestTapSkill:
    def test_defaults(self):
        skill = TapSkill(name="test", version="1.0", author="dev")
        assert skill.tags == []
        assert skill.depends_on == []
        assert skill.actions == []


class TestTapRegistry:
    def test_add_and_list(self):
        registry = TapRegistry()
        registry.add("user/repo", "https://github.com/user/repo")
        taps = registry.list()
        assert len(taps) == 1
        assert taps[0].name == "user/repo"

    def test_remove(self):
        registry = TapRegistry()
        registry.add("user/repo", "https://github.com/user/repo")
        registry.remove("user/repo")
        assert len(registry.list()) == 0

    @pytest.mark.asyncio
    async def test_search_stub(self):
        registry = TapRegistry()
        results = await registry.search("test")
        assert results == []  # stub returns empty
