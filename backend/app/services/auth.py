"""Authentication and User business logic."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, UnauthorizedError
from app.core.security import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
)
from app.models.user import User
from app.repositories.user import user_repo
from app.schemas.user import Token, UserCreate


class AuthService:
    """Service layer for authentication."""

    async def register_user(self, session: AsyncSession, *, user_in: UserCreate) -> User:
        """Register a new user."""
        existing_user = await user_repo.get_by_email_or_username(
            session, email=user_in.email, username=user_in.username
        )
        if existing_user:
            if existing_user.email == user_in.email:
                raise BadRequestError("Email already registered")
            raise BadRequestError("Username already taken")

        db_user = user_repo.create(
            session,
            obj_in={
                "email": user_in.email,
                "username": user_in.username,
                "hashed_password": hash_password(user_in.password),
            },
        )
        await session.commit()
        await session.refresh(db_user)
        return db_user

    async def authenticate_user(self, session: AsyncSession, *, email: str, password: str) -> User:
        """Authenticate user by email and password."""
        user = await user_repo.get_by_email(session, email=email)
        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Incorrect email or password")
        if not user.is_active:
            raise UnauthorizedError("User account is inactive")
        return user

    def generate_tokens(self, user: User) -> Token:
        """Generate access and refresh tokens for a user."""
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )


auth_service = AuthService()
