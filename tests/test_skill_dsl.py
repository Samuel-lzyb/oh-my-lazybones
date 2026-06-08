"""Tests for Skill DSL — Phase 2 (depends_on, actions, freeze)."""

import pytest

from server.models.skill import Skill


class TestSkillDSL:
    def test_depends_on_default(self):
        """New skill has empty depends_on (None before DB commit)."""
        skill = Skill(name="test", version="0.1.0", author="dev")
        assert skill.depends_on is None or skill.depends_on == []

    def test_depends_on_with_values(self):
        """Skill can declare dependencies."""
        skill = Skill(
            name="test", version="0.1.0", author="dev",
            depends_on=["python>=3.10", "requests"],
        )
        assert "python>=3.10" in skill.depends_on
        assert len(skill.depends_on) == 2

    def test_actions_default(self):
        """New skill has empty actions (None before DB commit)."""
        skill = Skill(name="test", version="0.1.0", author="dev")
        assert skill.actions is None or skill.actions == []

    def test_actions_with_values(self):
        """Skill can declare install actions."""
        skill = Skill(
            name="test", version="0.1.0", author="dev",
            actions=[{"type": "pip", "packages": ["requests"]}],
        )
        assert len(skill.actions) == 1
        assert skill.actions[0]["type"] == "pip"

    def test_freeze_prevents_changes(self):
        """Freeze makes skill immutable (except downloads)."""
        skill = Skill(name="test", version="0.1.0", author="dev")
        skill.freeze()
        assert skill.frozen is True
        with pytest.raises(AttributeError, match="frozen"):
            skill.name = "changed"

    def test_freeze_allows_downloads(self):
        """Downloads can still be updated after freeze."""
        skill = Skill(name="test", version="0.1.0", author="dev")
        skill.freeze()
        skill.downloads = 5  # should not raise

    def test_to_dict_includes_new_fields(self):
        """to_dict() includes depends_on and actions."""
        skill = Skill(
            name="test", version="0.1.0", author="dev",
            depends_on=["pkg-a"],
            actions=[{"type": "pip"}],
        )
        d = skill.to_dict()
        assert d["depends_on"] == ["pkg-a"]
        assert d["actions"] == [{"type": "pip"}]
