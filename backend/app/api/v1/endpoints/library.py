"""Library API endpoints.

Thin HTTP layer — all database/business logic lives in
:mod:`app.services.library`.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import CurrentUserID
from app.db.session import get_db
from app.schemas.music import AlbumResponse, ArtistResponse, TrackResponse
from app.schemas.pagination import Page
from app.services.library import build_page, library_service

router = APIRouter()


@router.get("/liked-songs", response_model=Page[TrackResponse])
async def get_liked_songs(
    current_user_id: CurrentUserID,
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
) -> Page[TrackResponse]:
    """List the current user's liked songs (newest first)."""
    tracks, total = await library_service.get_liked_songs(
        db, user_id=current_user_id, page=page, size=size
    )
    return build_page(
        [TrackResponse.model_validate(t) for t in tracks],
        total=total,
        page=page,
        size=size,
    )


@router.post("/liked-songs/{track_id}")
async def like_track(
    track_id: str,
    current_user_id: CurrentUserID,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """Like a track (idempotent). The track must already be cached locally."""
    await library_service.like_track(db, user_id=current_user_id, track_id=track_id)
    return {"status": "ok"}


@router.delete("/liked-songs/{track_id}", status_code=204)
async def unlike_track(
    track_id: str,
    current_user_id: CurrentUserID,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Remove a track from liked songs."""
    await library_service.unlike_track(db, user_id=current_user_id, track_id=track_id)


@router.get("/albums", response_model=Page[AlbumResponse])
async def get_saved_albums(
    current_user_id: CurrentUserID,
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
) -> Page[AlbumResponse]:
    """List the current user's saved albums (newest first)."""
    albums, total = await library_service.get_saved_albums(
        db, user_id=current_user_id, page=page, size=size
    )
    return build_page(
        [AlbumResponse.model_validate(a) for a in albums],
        total=total,
        page=page,
        size=size,
    )


@router.post("/albums/{album_id}")
async def save_album(
    album_id: str,
    current_user_id: CurrentUserID,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """Save an album (idempotent). The album must already be cached locally."""
    await library_service.save_album(db, user_id=current_user_id, album_id=album_id)
    return {"status": "ok"}


@router.delete("/albums/{album_id}", status_code=204)
async def unsave_album(
    album_id: str,
    current_user_id: CurrentUserID,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Remove an album from saved albums."""
    await library_service.unsave_album(db, user_id=current_user_id, album_id=album_id)


@router.get("/artists", response_model=Page[ArtistResponse])
async def get_followed_artists(
    current_user_id: CurrentUserID,
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
) -> Page[ArtistResponse]:
    """List the artists the current user follows (newest first)."""
    artists, total = await library_service.get_followed_artists(
        db, user_id=current_user_id, page=page, size=size
    )
    return build_page(
        [ArtistResponse.model_validate(a) for a in artists],
        total=total,
        page=page,
        size=size,
    )


@router.post("/artists/{artist_id}")
async def follow_artist(
    artist_id: str,
    current_user_id: CurrentUserID,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """Follow an artist (idempotent). The artist must already be cached locally."""
    await library_service.follow_artist(db, user_id=current_user_id, artist_id=artist_id)
    return {"status": "ok"}


@router.delete("/artists/{artist_id}", status_code=204)
async def unfollow_artist(
    artist_id: str,
    current_user_id: CurrentUserID,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Unfollow an artist."""
    await library_service.unfollow_artist(db, user_id=current_user_id, artist_id=artist_id)


@router.get("/history", response_model=Page[TrackResponse])
async def get_play_history(
    current_user_id: CurrentUserID,
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
) -> Page[TrackResponse]:
    """List the current user's play history (most recent first)."""
    tracks, total = await library_service.get_play_history(
        db, user_id=current_user_id, page=page, size=size
    )
    return build_page(
        [TrackResponse.model_validate(t) for t in tracks],
        total=total,
        page=page,
        size=size,
    )


@router.post("/history/{track_id}")
async def add_play_history(
    track_id: str,
    current_user_id: CurrentUserID,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """Record that the user played a track."""
    await library_service.add_play_history(db, user_id=current_user_id, track_id=track_id)
    return {"status": "ok"}
