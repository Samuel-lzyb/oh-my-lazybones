"""Skill ORM model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Skill(Base):
    """A registered Agent Skill."""

    __tablename__ = "skills"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, index=True
    )
    version: Mapped[str] = mapped_column(
        String(16), nullable=False, default="0.1.0"
    )
    author: Mapped[str] = mapped_column(
        String(64), nullable=False, index=True
    )
    description: Mapped[str] = mapped_column(
        Text, nullable=False, default=""
    )
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    downloads: Mapped[int] = mapped_column(Integer, default=0)
    depends_on: Mapped[list[str]] = mapped_column(
        JSON, nullable=False, default=lambda: []
    )
    actions: Mapped[list[dict]] = mapped_column(
        JSON, nullable=False, default=lambda: []
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    _frozen: bool = False

    def freeze(self) -> None:
        """Make this skill immutable. No further attribute changes allowed."""
        self._frozen = True

    def __setattr__(self, name: str, value) -> None:
        if getattr(self, "_frozen", False) and name not in (
            "_frozen", "downloads", "updated_at"
        ):
            raise AttributeError(f"Skill '{self.name}' is frozen")
        super().__setattr__(name, value)

    @property
    def frozen(self) -> bool:
        return self._frozen

    def to_dict(self) -> dict:
        """Convert to plain dict for serialization / search indexing."""
        return {
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "description": self.description,
            "tags": self.tags or [],
            "downloads": self.downloads or 0,
            "depends_on": self.depends_on or [],
            "actions": self.actions or [],
            "created_at": str(self.created_at) if self.created_at else "",
        }
