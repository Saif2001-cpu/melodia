"""Music API endpoints bridging the provider to the frontend."""


from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.core.deps import CurrentUserID
from app.providers.base import MusicProvider, SearchResults, TrackData, AlbumData, ArtistData
from app.providers.factory import get_music_provider
from app.services.library import library_service

router = APIRouter()


@router.get("/search", response_model=SearchResults)
async def search_music(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0),
    provider: MusicProvider = Depends(get_music_provider),
    # Require auth so users must be logged in to search
    current_user_id: CurrentUserID = None,  # noqa: UP007 — dependency only
) -> SearchResults:
    """Search for tracks, albums, and artists."""
    return await provider.search(query=q, limit=limit, offset=offset)


@router.get("/trending", response_model=list[TrackData])
async def get_trending_tracks(
    limit: int = Query(20, ge=1, le=50),
    provider: MusicProvider = Depends(get_music_provider),
    current_user_id: CurrentUserID = None,  # noqa: UP007
) -> list[TrackData]:
    """Get globally trending tracks."""
    return await provider.get_trending(limit=limit)


@router.get("/tracks/{track_id}", response_model=TrackData)
async def get_track(
    track_id: str,
    provider: MusicProvider = Depends(get_music_provider),
    current_user_id: CurrentUserID = None,  # noqa: UP007
) -> TrackData:
    """Get details for a specific track."""
    return await provider.get_track(track_id)


@router.get("/albums/{album_id}", response_model=AlbumData)
async def get_album(
    album_id: str,
    provider: MusicProvider = Depends(get_music_provider),
    current_user_id: CurrentUserID = None,  # noqa: UP007
) -> AlbumData:
    """Get details and tracks for a specific album."""
    return await provider.get_album(album_id)


@router.get("/artists/{artist_id}", response_model=ArtistData)
async def get_artist(
    artist_id: str,
    provider: MusicProvider = Depends(get_music_provider),
    current_user_id: CurrentUserID = None,  # noqa: UP007
) -> ArtistData:
    """Get details, top tracks, and albums for a specific artist."""
    return await provider.get_artist(artist_id)


@router.get("/recommendations", response_model=list[TrackData])
async def get_recommendations(
    limit: int = Query(20, ge=1, le=50),
    provider: MusicProvider = Depends(get_music_provider),
    db: AsyncSession = Depends(get_db),
    current_user_id: CurrentUserID = None,  # noqa: UP007
) -> list[TrackData]:
    """Get personalized track recommendations based on recent play history.

    Strategy: recommend the top tracks of the artist from the user's most
    recently played track; fall back to global trending when there is no
    history (or the lookup fails).
    """
    last_played = await library_service.get_last_played_track(db, user_id=current_user_id)
    if last_played and last_played.artist_id:
        try:
            tracks = await provider.get_artist_top_tracks(last_played.artist_id, limit=limit)
            if tracks:
                return tracks
        except Exception:  # pragma: no cover - provider/network failure
            pass

    return await provider.get_trending(limit=limit)
