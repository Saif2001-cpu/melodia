"""Pagination utilities used across API endpoints."""

from dataclasses import dataclass
from typing import Generic, TypeVar

from fastapi import Query
from pydantic import BaseModel

T = TypeVar("T")


class PaginationParams(BaseModel):
    """Query parameter model for paginated endpoints."""

    page: int = Query(default=1, ge=1, description="Page number (1-indexed)")
    size: int = Query(default=20, ge=1, le=100, description="Items per page")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size


@dataclass
class Page(Generic[T]):
    """Paginated response envelope."""

    items: list[T]
    total: int
    page: int
    size: int

    @property
    def pages(self) -> int:
        if self.size == 0:
            return 0
        return -(-self.total // self.size)  # ceiling division

    @property
    def has_next(self) -> bool:
        return self.page < self.pages

    @property
    def has_prev(self) -> bool:
        return self.page > 1

    def to_dict(self) -> dict:
        return {
            "items": self.items,
            "total": self.total,
            "page": self.page,
            "size": self.size,
            "pages": self.pages,
            "has_next": self.has_next,
            "has_prev": self.has_prev,
        }
