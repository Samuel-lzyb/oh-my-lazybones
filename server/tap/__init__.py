"""Tap system — third-party Skill repositories via Git.

Phase 3 architecture stubs. Full implementation deferred to M7.

Pattern: Homebrew's Tap system (tap.rb ~1300 lines).
A Tap is a Git repository containing Skill definitions in YAML.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TapInfo:
    """Metadata for a registered Tap."""

    name: str  # "samuel-lzyb/agent-skills"
    url: str  # Git clone URL
    path: Path  # Local checkout path
    enabled: bool = True

    @property
    def user(self) -> str:
        return self.name.split("/")[0]

    @property
    def repo(self) -> str:
        return self.name.split("/")[1]


@dataclass
class TapSkill:
    """A Skill discovered from a Tap repository (YAML-parsed)."""

    name: str
    version: str
    author: str
    description: str = ""
    tags: list[str] = field(default_factory=list)
    depends_on: list[str] = field(default_factory=list)
    actions: list[dict] = field(default_factory=list)
    tap: str = ""  # source tap name


class TapRegistry:
    """Manages installed Taps. Phase 3 stub."""

    def __init__(self, base_path: Path | None = None):
        self.base_path = base_path or Path.home() / ".lazybones" / "taps"
        self._taps: dict[str, TapInfo] = {}

    def add(self, name: str, url: str) -> TapInfo:
        """Add a Tap (stub — no Git clone yet)."""
        info = TapInfo(
            name=name,
            url=url,
            path=self.base_path / name.replace("/", "-"),
        )
        self._taps[name] = info
        return info

    def remove(self, name: str) -> None:
        """Remove a Tap."""
        self._taps.pop(name, None)

    def list(self) -> list[TapInfo]:
        """List all registered Taps."""
        return list(self._taps.values())

    async def search(self, query: str, limit: int = 10) -> list[TapSkill]:
        """Search across all Taps (stub — no implementation)."""
        return []  # M7: parse YAML files from each tap
