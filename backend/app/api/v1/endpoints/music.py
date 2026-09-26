"""Music API endpoints bridging the provider to the frontend."""


from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.core.deps import get_current_user_id, get_music_provider
from app.models.library import PlayHistory
from app.providers.base import (
    AlbumData,
    ArtistData,
    MusicProvider,
    SearchResults,
    TrackData,
)

router = APIRouter()


@router.get("/search", response_model=SearchResults)
async def search_music(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(20, ge=1, le=50),
    offset: int = Query(0, ge=0),
    provider: MusicProvider = Depends(get_music_provider),
    # Require auth so users must be logged in to search
    current_user_id: str = Depends(get_current_user_id),
) -> SearchResults:
    """Search for tracks, albums, and artists."""
    return await provider.search(query=q, limit=limit, offset=offset)


@router.get("/trending", response_model=list[TrackData])
async def get_trending_tracks(
    limit: int = Query(20, ge=1, le=50),
    provider: MusicProvider = Depends(get_music_provider),
    current_user_id: str = Depends(get_current_user_id),
) -> list[TrackData]:
    """Get globally trending tracks."""
    return await provider.get_trending(limit=limit)


@router.get("/tracks/{track_id}", response_model=TrackData)
async def get_track(
    track_id: str,
    provider: MusicProvider = Depends(get_music_provider),
    current_user_id: str = Depends(get_current_user_id),
) -> TrackData:
    """Get details for a specific track."""
    return await provider.get_track(track_id)


@router.get("/albums/{album_id}", response_model=AlbumData)
async def get_album(
    album_id: str,
    provider: MusicProvider = Depends(get_music_provider),
    current_user_id: str = Depends(get_current_user_id),
) -> AlbumData:
    """Get details and tracks for a specific album."""
    return await provider.get_album(album_id)


@router.get("/artists/{artist_id}", response_model=ArtistData)
async def get_artist(
    artist_id: str,
    provider: MusicProvider = Depends(get_music_provider),
    current_user_id: str = Depends(get_current_user_id),
) -> ArtistData:
    """Get details, top tracks, and albums for a specific artist."""
    return await provider.get_artist(artist_id)


@router.get("/recommendations", response_model=list[TrackData])
async def get_recommendations(
    limit: int = Query(20, ge=1, le=50),
    provider: MusicProvider = Depends(get_music_provider),
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
) -> list[TrackData]:
    """Get personalized track recommendations based on recent play history."""
    # Find the most recently played track
    query = (
        select(PlayHistory)
        .where(PlayHistory.user_id == current_user_id)
        .options(selectinload(PlayHistory.track))
        .order_by(PlayHistory.played_at.desc())
        .limit(1)
    )
    result = await db.execute(query)
    last_played = result.scalar_one_or_none()

    if last_played and last_played.track:
        # Fetch the top tracks for this artist as a basic recommendation strategy
        # In a real system, you'd use a more sophisticated recommendation engine
        artist_id = last_played.track.artist_id
        if artist_id:
            try:
                tracks = await provider.get_artist_top_tracks(artist_id, limit=limit)
                if tracks:
                    # Filter out the track they already played if possible, or just return
                    return tracks
            except Exception:
                pass

    # Fallback to trending
    return await provider.get_trending(limit=limit)
