"""Tests for hierarchical exception system — Phase 1."""

import pytest

from server.exceptions import (
    LazybonesError,
    SearchBackendError,
    SkillConflictError,
    SkillNotFoundError,
    ValidationError,
    suggest_name,
)


class TestExceptions:
    def test_base_exception(self):
        """T1: LazybonesError has exit_code."""
        exc = LazybonesError()
        assert exc.exit_code == 1

    def test_skill_not_found_basic(self):
        """T1: SkillNotFoundError without suggestions."""
        exc = SkillNotFoundError("foo")
        assert "Skill 'foo' not found" in str(exc)
        assert exc.exit_code == 2

    def test_skill_not_found_with_suggestions(self):
        """T2: SkillNotFoundError with Did-you-mean."""
        exc = SkillNotFoundError("emal", ["email", "emacs", "emerald"])
        assert "Did you mean: email, emacs, emerald" in str(exc)

    def test_skill_not_found_suggestions_exclude_self(self):
        """T2: Suggestions exclude the query name itself."""
        exc = SkillNotFoundError("foo", ["foo", "food", "fool"])
        # Suggestions should not include the query name itself
        suggestion_part = str(exc).split("Did you mean: ")[-1].rstrip("?")
        suggested_names = [s.strip() for s in suggestion_part.split(",")]
        assert "food" in suggested_names
        assert "foo" not in suggested_names

    def test_skill_conflict(self):
        """T3: SkillConflictError."""
        exc = SkillConflictError("bar")
        assert "Skill 'bar' already exists" in str(exc)
        assert exc.exit_code == 3

    def test_validation_error(self):
        """T4: ValidationError."""
        exc = ValidationError("invalid input")
        assert exc.exit_code == 4

    def test_search_backend_error(self):
        """T4: SearchBackendError."""
        exc = SearchBackendError("meilisearch down")
        assert exc.exit_code == 5

    def test_all_inherit_from_base(self):
        """T4: All exceptions inherit from LazybonesError."""
        assert isinstance(SkillNotFoundError("x"), LazybonesError)
        assert isinstance(SkillConflictError("x"), LazybonesError)
        assert isinstance(ValidationError("x"), LazybonesError)
        assert isinstance(SearchBackendError("x"), LazybonesError)


class TestSuggestName:
    def test_exact_match(self):
        result = suggest_name("email", ["email", "emacs"])
        assert "email" in result  # exact match always included

    def test_close_match(self):
        result = suggest_name("emal", ["email", "daily-email-digest", "weather"])
        assert "email" in result or "daily-email-digest" in result

    def test_no_match(self):
        assert suggest_name("xyzabc", ["email", "weather"]) == []

    def test_empty_candidates(self):
        assert suggest_name("test", []) == []
