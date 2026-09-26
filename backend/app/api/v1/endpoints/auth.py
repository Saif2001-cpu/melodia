"""Authentication API endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import CurrentUserID, get_current_user_id_from_refresh
from app.core.exceptions import NotFoundError, UnauthorizedError
from app.db.session import get_db
from app.models.user import User
from app.repositories.user import user_repo
from app.schemas.user import Token, UserCreate, UserLogin, UserResponse
from app.services.auth import auth_service

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
)
async def register(
    user_in: UserCreate,
    session: AsyncSession = Depends(get_db),
) -> User:
    """Register a new user with email, username, and password."""
    user = await auth_service.register_user(session, user_in=user_in)
    return user


@router.post(
    "/login",
    response_model=Token,
    summary="Login via JSON body",
)
async def login_json(
    credentials: UserLogin,
    session: AsyncSession = Depends(get_db),
) -> Token:
    """Authenticate user and return JWT tokens via JSON payload."""
    user = await auth_service.authenticate_user(
        session, email=credentials.email, password=credentials.password
    )
    return auth_service.generate_tokens(user)


@router.post(
    "/token",
    response_model=Token,
    summary="OAuth2 compatible token login",
    include_in_schema=False,
)
async def login_oauth2(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_db),
) -> Token:
    """Authenticate user and return JWT tokens via form-data (for Swagger)."""
    user = await auth_service.authenticate_user(
        session, email=form_data.username, password=form_data.password
    )
    return auth_service.generate_tokens(user)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
)
async def get_current_user(
    user_id: CurrentUserID,
    session: AsyncSession = Depends(get_db),
) -> User:
    """Get the currently authenticated user's profile."""
    user = await user_repo.get(session, id=user_id)
    if not user:
        raise NotFoundError("User not found")
    if not user.is_active:
        raise UnauthorizedError("User is inactive")
    return user


@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh access token",
)
async def refresh_token(
    user_id: Annotated[str, Depends(get_current_user_id_from_refresh)],
    session: AsyncSession = Depends(get_db),
) -> Token:
    """Generate new access and refresh tokens from a valid refresh token."""
    user = await user_repo.get(session, id=user_id)
    if not user:
        raise UnauthorizedError("User not found")
    if not user.is_active:
        raise UnauthorizedError("User is inactive")
    return auth_service.generate_tokens(user)
