"""Playlist API endpoints.

Thin HTTP layer — business logic and authorization live in
:mod:`app.services.playlist`; realtime fan-out lives in
:mod:`app.core.websockets`.
"""

from fastapi import APIRouter, Depends, Query, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import CurrentUserID
from app.core.websockets import manager
from app.db.session import get_db
from app.schemas.pagination import Page
from app.schemas.playlist import PlaylistCreate, PlaylistResponse
from app.services.library import build_page
from app.services.playlist import playlist_repo, playlist_service

router = APIRouter()


class AddTrackRequest(BaseModel):
    """Body for adding a track to a playlist."""

    track_id: str = Field(..., min_length=1)


class ReorderTracksRequest(BaseModel):
    """Body for reordering playlist tracks by explicit track-id order."""

    track_ids: list[str] = Field(default_factory=list)


def _to_response(playlist, *, track_count: int | None = None) -> PlaylistResponse:
    """Build a PlaylistResponse with derived fields populated."""
    response = PlaylistResponse.model_validate(playlist)
    response.owner_name = playlist.owner.username
    response.track_count = track_count if track_count is not None else len(playlist.tracks)
    return response


@router.get("", response_model=Page[PlaylistResponse])
async def get_playlists(
    current_user_id: CurrentUserID,
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
) -> Page[PlaylistResponse]:
    """List playlists owned by the current user (newest first)."""
    total = await playlist_repo.count_for_owner(db, owner_id=current_user_id)
    playlists = await playlist_repo.list_for_owner(
        db, owner_id=current_user_id, offset=(page - 1) * size, limit=size
    )
    return build_page(
        [_to_response(p) for p in playlists], total=total, page=page, size=size
    )


@router.post("", response_model=PlaylistResponse, status_code=201)
async def create_playlist(
    playlist_in: PlaylistCreate,
    current_user_id: CurrentUserID,
    db: AsyncSession = Depends(get_db),
) -> PlaylistResponse:
    """Create a new empty playlist owned by the current user."""
    playlist = await playlist_service.create_playlist(
        db,
        user_id=current_user_id,
        name=playlist_in.name,
        description=playlist_in.description,
        is_public=playlist_in.is_public,
        is_collaborative=playlist_in.is_collaborative,
    )
    return _to_response(playlist, track_count=0)


@router.get("/{playlist_id}", response_model=PlaylistResponse)
async def get_playlist(
    playlist_id: str,
    current_user_id: CurrentUserID,
    db: AsyncSession = Depends(get_db),
) -> PlaylistResponse:
    """Get a playlist with its tracks (private playlists: owner only)."""
    playlist = await playlist_repo.get_for_user(db, playlist_id=playlist_id)
    playlist_service.check_view_access(playlist, current_user_id)
    return _to_response(playlist)


@router.delete("/{playlist_id}", status_code=204)
async def delete_playlist(
    playlist_id: str,
    current_user_id: CurrentUserID,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a playlist (owner only)."""
    await playlist_service.delete_playlist(db, playlist_id=playlist_id, user_id=current_user_id)


@router.post("/{playlist_id}/tracks", status_code=201)
async def add_track(
    playlist_id: str,
    payload: AddTrackRequest,
    current_user_id: CurrentUserID,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """Add a track to a playlist (owner or collaborator). Idempotent."""
    await playlist_service.add_track(
        db, playlist_id=playlist_id, track_id=payload.track_id, user_id=current_user_id
    )
    await manager.broadcast_to_playlist(
        playlist_id,
        {"event": "track_added", "playlist_id": playlist_id, "track_id": payload.track_id},
    )
    return {"status": "ok"}


@router.delete("/{playlist_id}/tracks/{track_id}", status_code=204)
async def remove_track(
    playlist_id: str,
    track_id: str,
    current_user_id: CurrentUserID,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Remove a track from a playlist (owner or collaborator)."""
    await playlist_service.remove_track(
        db, playlist_id=playlist_id, track_id=track_id, user_id=current_user_id
    )
    await manager.broadcast_to_playlist(
        playlist_id,
        {"event": "track_removed", "playlist_id": playlist_id, "track_id": track_id},
    )


@router.put("/{playlist_id}/tracks/reorder")
async def reorder_tracks(
    playlist_id: str,
    payload: ReorderTracksRequest,
    current_user_id: CurrentUserID,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """Reorder playlist tracks by providing the desired track-id order."""
    await playlist_service.reorder_tracks(
        db, playlist_id=playlist_id, track_ids=payload.track_ids, user_id=current_user_id
    )
    await manager.broadcast_to_playlist(
        playlist_id, {"event": "tracks_reordered", "playlist_id": playlist_id}
    )
    return {"status": "ok"}


@router.websocket("/{playlist_id}/ws")
async def playlist_websocket(websocket: WebSocket, playlist_id: str) -> None:
    """Realtime channel notifying clients about playlist modifications."""
    await manager.connect(websocket, playlist_id)
    try:
        while True:
            # Clients don't send meaningful messages; reads keep the socket alive.
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, playlist_id)
