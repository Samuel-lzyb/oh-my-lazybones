"""Shared Pydantic schemas."""

from typing import Generic, List, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated list response."""

    items: List[T]
    total: int
    page: int
    limit: int


class ErrorDetail(BaseModel):
    """Structured error."""

    code: str
    message: str
