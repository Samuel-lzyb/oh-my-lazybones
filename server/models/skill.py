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
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
