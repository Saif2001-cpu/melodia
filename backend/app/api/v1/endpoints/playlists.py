from fastapi import APIRouter, Depends, HTTPException, Query, status, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.core.deps import get_current_user_id
from app.models.playlist import Playlist, PlaylistTrack
from app.models.track import Track
from app.models.user import User
from app.schemas.playlist import (
    PlaylistCreate,
    PlaylistUpdate,
    PlaylistResponse,
)
from app.schemas.pagination import Page
from typing import List

from app.core.websockets import manager

router = APIRouter()

@router.get("", response_model=Page[PlaylistResponse])
async def get_playlists(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    offset = (page - 1) * size
    
    # Get total count
    count_query = select(Playlist).where(Playlist.owner_id == current_user_id)
    total_result = await db.execute(count_query)
    total = len(total_result.unique().all())
    
    # Get items
    query = (
        select(Playlist)
        .where(Playlist.owner_id == current_user_id)
        .options(selectinload(Playlist.owner), selectinload(Playlist.tracks).selectinload(PlaylistTrack.track))
        .order_by(Playlist.created_at.desc())
        .offset(offset)
        .limit(size)
    )
    result = await db.execute(query)
    playlists = result.scalars().unique().all()
    
    items = []
    for p in playlists:
        pr = PlaylistResponse.model_validate(p)
        pr.owner_name = p.owner.username
        pr.track_count = len(p.tracks)
        items.append(pr)
        
    pages = (total + size - 1) // size
    return Page[PlaylistResponse](
        items=items,
        total=total,
        page=page,
        size=size,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1,
    )

@router.post("", response_model=PlaylistResponse)
async def create_playlist(
    playlist_in: PlaylistCreate,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    user_query = select(User).where(User.id == current_user_id)
    user_result = await db.execute(user_query)
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    db_playlist = Playlist(
        name=playlist_in.name,
        description=playlist_in.description,
        is_public=playlist_in.is_public,
        is_collaborative=playlist_in.is_collaborative,
        owner_id=current_user_id,
    )
    db.add(db_playlist)
    await db.commit()
    await db.refresh(db_playlist)
    
    pr = PlaylistResponse.model_validate(db_playlist)
    pr.owner_name = user.username
    return pr

@router.get("/{playlist_id}", response_model=PlaylistResponse)
async def get_playlist(
    playlist_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    query = (
        select(Playlist)
        .where(Playlist.id == playlist_id)
        .options(selectinload(Playlist.owner), selectinload(Playlist.tracks).selectinload(PlaylistTrack.track))
    )
    result = await db.execute(query)
    playlist = result.scalar_one_or_none()
    
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
        
    if not playlist.is_public and playlist.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to view this playlist")
        
    pr = PlaylistResponse.model_validate(playlist)
    pr.owner_name = playlist.owner.username
    pr.track_count = len(playlist.tracks)
    return pr

@router.delete("/{playlist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_playlist(
    playlist_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    query = select(Playlist).where(Playlist.id == playlist_id)
    result = await db.execute(query)
    playlist = result.scalar_one_or_none()
    
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
        
    if playlist.owner_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this playlist")
        
    await db.delete(playlist)
    await db.commit()

@router.post("/{playlist_id}/tracks")
async def add_track(
    playlist_id: str,
    payload: dict,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    track_id = payload.get("track_id")
    if not track_id:
        raise HTTPException(status_code=400, detail="track_id is required")
        
    query = select(Playlist).where(Playlist.id == playlist_id).options(selectinload(Playlist.tracks))
    result = await db.execute(query)
    playlist = result.scalar_one_or_none()
    
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
        
    if playlist.owner_id != current_user_id and not playlist.is_collaborative:
        raise HTTPException(status_code=403, detail="Not authorized to modify this playlist")
        
    # Ensure track exists in local DB. If not, ideally fetch from provider and save it. 
    # For now, let's assume it was added via trending/search which saves it or we just create a dummy one.
    track_query = select(Track).where(Track.id == track_id)
    track_result = await db.execute(track_query)
    track = track_result.scalar_one_or_none()
    
    if not track:
        # We should ideally call get_music_provider() to fetch and save.
        raise HTTPException(status_code=404, detail="Track not found in local database. Please fetch it first.")

    # Check if already in playlist
    if any(pt.track_id == track_id for pt in playlist.tracks):
        return {"status": "ok"}
        
    pt = PlaylistTrack(
        playlist_id=playlist_id,
        track_id=track_id,
        position=len(playlist.tracks),
        added_by_id=current_user_id,
    )
    db.add(pt)
    await db.commit()
    
    # Broadcast update
    await manager.broadcast_to_playlist(
        playlist_id,
        {"event": "track_added", "playlist_id": playlist_id, "track_id": track_id}
    )
    
    return {"status": "ok"}
@router.delete("/{playlist_id}/tracks/{track_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_track(
    playlist_id: str,
    track_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    query = select(Playlist).where(Playlist.id == playlist_id)
    result = await db.execute(query)
    playlist = result.scalar_one_or_none()
    
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
        
    if playlist.owner_id != current_user_id and not playlist.is_collaborative:
        raise HTTPException(status_code=403, detail="Not authorized to modify this playlist")
        
    pt_query = select(PlaylistTrack).where(PlaylistTrack.playlist_id == playlist_id, PlaylistTrack.track_id == track_id)
    pt_result = await db.execute(pt_query)
    pt = pt_result.scalar_one_or_none()
    
    if pt:
        await db.delete(pt)
        
        # update positions of subsequent tracks
        update_query = (
            select(PlaylistTrack)
            .where(PlaylistTrack.playlist_id == playlist_id, PlaylistTrack.position > pt.position)
        )
        res = await db.execute(update_query)
        for sub_pt in res.scalars().all():
            sub_pt.position -= 1
            
        await db.commit()
        
        # Broadcast update
        await manager.broadcast_to_playlist(
            playlist_id,
            {"event": "track_removed", "playlist_id": playlist_id, "track_id": track_id}
        )

@router.put("/{playlist_id}/tracks/reorder")
async def reorder_tracks(
    playlist_id: str,
    payload: dict,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    # payload: {"track_ids": ["id1", "id2", ...]}
    track_ids = payload.get("track_ids", [])
    
    query = select(Playlist).where(Playlist.id == playlist_id).options(selectinload(Playlist.tracks))
    result = await db.execute(query)
    playlist = result.scalar_one_or_none()
    
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")
        
    if playlist.owner_id != current_user_id and not playlist.is_collaborative:
        raise HTTPException(status_code=403, detail="Not authorized to modify this playlist")
        
    # Map track_id -> PlaylistTrack
    pt_map = {pt.track_id: pt for pt in playlist.tracks}
    
    # Update positions
    for i, tid in enumerate(track_ids):
        if tid in pt_map:
            pt_map[tid].position = i
            
    await db.commit()
    
    # Broadcast update
    await manager.broadcast_to_playlist(
        playlist_id,
        {"event": "tracks_reordered", "playlist_id": playlist_id}
    )
    
    return {"status": "ok"}


@router.websocket("/{playlist_id}/ws")
async def websocket_endpoint(websocket: WebSocket, playlist_id: str):
    await manager.connect(websocket, playlist_id)
    try:
        while True:
            # We don't expect messages from client for now, just keep connection open
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, playlist_id)

