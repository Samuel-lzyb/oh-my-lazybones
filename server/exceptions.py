"""Hierarchical exception system for oh-my-lazybones.

Pattern: Homebrew's exceptions.rb — typed errors with exit codes,
meaningful messages, and "Did you mean?" suggestions.
"""

import difflib
from typing import Sequence


class LazybonesError(Exception):
    """Base exception for all oh-my-lazybones errors."""

    exit_code: int = 1


class SkillNotFoundError(LazybonesError):
    """Skill not found, with optional fuzzy-match suggestions."""

    exit_code = 2

    def __init__(self, name: str, suggestions: Sequence[str] | None = None):
        msg = f"Skill '{name}' not found"
        if suggestions:
            narrowed = [s for s in suggestions if s != name][:3]
            if narrowed:
                msg += f". Did you mean: {', '.join(narrowed)}?"
        self.message = msg
        super().__init__(msg)


class SkillConflictError(LazybonesError):
    """Skill already exists (duplicate name on publish)."""

    exit_code = 3

    def __init__(self, name: str):
        msg = f"Skill '{name}' already exists"
        self.message = msg
        super().__init__(msg)


class ValidationError(LazybonesError):
    """Input validation failed."""

    exit_code = 4


class SearchBackendError(LazybonesError):
    """Search backend unavailable."""

    exit_code = 5


def suggest_name(
    query: str, candidates: Sequence[str], limit: int = 3
) -> list[str]:
    """Find candidate names close to query via fuzzy matching."""
    return difflib.get_close_matches(
        query, list(candidates), n=limit, cutoff=0.6
    )
