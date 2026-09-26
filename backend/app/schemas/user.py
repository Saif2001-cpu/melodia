"""User and Authentication schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class Token(BaseModel):
    """OAuth2 standard token response schema."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """JWT token payload schema."""

    sub: str | None = None
    exp: int | None = None
    type: str | None = None


class UserBase(BaseModel):
    """Base user schema with common attributes."""

    email: EmailStr
    username: str = Field(min_length=3, max_length=50)


class UserCreate(UserBase):
    """User registration schema."""

    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    """User login schema (alternative to form data)."""

    email: EmailStr
    password: str


class UserResponse(UserBase):
    """User response schema."""

    id: str
    is_active: bool
    is_superuser: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
