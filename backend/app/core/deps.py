"""FastAPI dependency injection helpers."""

from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import decode_token

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)] = None,
) -> str:
    """Extract and validate the Bearer JWT, return the user_id string."""
    from app.core.exceptions import UnauthorizedError

    if credentials is None:
        raise UnauthorizedError("Missing authorization header")
    return decode_token(credentials.credentials, expected_type="access")


async def get_current_user_id_from_refresh(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)] = None,
) -> str:
    """Extract and validate the Bearer JWT refresh token, return the user_id string."""
    from app.core.exceptions import UnauthorizedError

    if credentials is None:
        raise UnauthorizedError("Missing authorization header")
    return decode_token(credentials.credentials, expected_type="refresh")


async def get_current_user_uuid(
    user_id: Annotated[str, Depends(get_current_user_id)],
) -> UUID:
    """Same as get_current_user_id but returns a UUID."""
    try:
        return UUID(user_id)
    except ValueError:
        from app.core.exceptions import UnauthorizedError

        raise UnauthorizedError("Invalid token subject") from None


CurrentUserID = Annotated[str, Depends(get_current_user_id)]
CurrentUserUUID = Annotated[UUID, Depends(get_current_user_uuid)]


_music_provider = None


async def get_music_provider():
    """Dependency to inject the MusicProvider (Deezer) as a module-level singleton."""
    global _music_provider
    from app.providers.deezer import DeezerProvider

    if _music_provider is None:
        _music_provider = DeezerProvider()
    return _music_provider
