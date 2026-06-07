"""Schema validation tests."""

import pytest
from pydantic import ValidationError

from server.schemas.skill import SkillCreate, SkillSearchParams


class TestSkillCreate:
    def test_valid_minimal(self):
        s = SkillCreate(name="my-skill", author="dev")
        assert s.name == "my-skill"
        assert s.version == "0.1.0"
        assert s.tags == []

    def test_valid_full(self):
        s = SkillCreate(
            name="full-skill", version="1.2.3", author="dev",
            description="desc", tags=["a", "b"],
        )
        assert s.version == "1.2.3"
        assert len(s.tags) == 2

    def test_name_too_short(self):
        with pytest.raises(ValidationError):
            SkillCreate(name="ab", author="dev")

    def test_name_too_long(self):
        with pytest.raises(ValidationError):
            SkillCreate(name="a" * 65, author="dev")

    def test_name_invalid_chars(self):
        with pytest.raises(ValidationError):
            SkillCreate(name="INVALID NAME", author="dev")

    def test_tags_too_many(self):
        with pytest.raises(ValidationError):
            SkillCreate(name="test", author="dev", tags=[f"t{i}" for i in range(11)])

    def test_description_too_long(self):
        with pytest.raises(ValidationError):
            SkillCreate(name="test", author="dev", description="x" * 2001)


class TestSkillSearchParams:
    def test_defaults(self):
        params = SkillSearchParams()
        assert params.page == 1
        assert params.limit == 20
        assert params.sort == "downloads"

    def test_limit_out_of_range(self):
        with pytest.raises(ValidationError):
            SkillSearchParams(limit=200)

    def test_page_negative(self):
        with pytest.raises(ValidationError):
            SkillSearchParams(page=0)
