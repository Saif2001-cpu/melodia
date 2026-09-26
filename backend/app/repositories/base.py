"""Base repository with generic CRUD operations."""

from collections.abc import Sequence
from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic repository for basic CRUD."""

    def __init__(self, model: type[ModelType]):
        """Initialize with a SQLAlchemy model class."""
        self.model = model

    async def get(self, session: AsyncSession, id: Any) -> ModelType | None:
        """Get a single record by primary key."""
        result = await session.execute(select(self.model).where(self.model.id == id))
        return result.scalars().first()

    async def get_all(
        self, session: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> Sequence[ModelType]:
        """Get all records, optionally paginated."""
        result = await session.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    def create(self, session: AsyncSession, *, obj_in: dict[str, Any]) -> ModelType:
        """Create a new record. Call session.commit() afterwards."""
        db_obj = self.model(**obj_in)
        session.add(db_obj)
        return db_obj

    async def update(
        self, session: AsyncSession, *, db_obj: ModelType, obj_in: dict[str, Any]
    ) -> ModelType:
        """Update an existing record. Call session.commit() afterwards."""
        for field, value in obj_in.items():
            setattr(db_obj, field, value)
        session.add(db_obj)
        return db_obj

    async def delete(self, session: AsyncSession, *, id: Any) -> ModelType | None:
        """Delete a record by primary key. Call session.commit() afterwards."""
        obj = await self.get(session, id=id)
        if obj:
            await session.delete(obj)
        return obj
