"""User repository."""

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    """Repository for User model."""

    async def get_by_email(self, session: AsyncSession, *, email: str) -> User | None:
        """Get a user by email."""
        result = await session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_by_username(self, session: AsyncSession, *, username: str) -> User | None:
        """Get a user by username."""
        result = await session.execute(select(User).where(User.username == username))
        return result.scalars().first()

    async def get_by_email_or_username(
        self, session: AsyncSession, *, email: str, username: str
    ) -> User | None:
        """Check if email or username is already taken."""
        result = await session.execute(
            select(User).where(or_(User.email == email, User.username == username))
        )
        return result.scalars().first()


user_repo = UserRepository(User)
