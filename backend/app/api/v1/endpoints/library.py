from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.core.deps import get_current_user_id
from app.models.library import LikedSong, SavedAlbum, FollowedArtist, PlayHistory
from app.models.track import Track, Album, Artist
from app.schemas.music import TrackResponse, AlbumResponse, ArtistResponse
from app.schemas.pagination import Page

router = APIRouter()

@router.get("/liked-songs", response_model=Page[TrackResponse])
async def get_liked_songs(
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    offset = (page - 1) * size
    
    count_query = select(LikedSong).where(LikedSong.user_id == current_user_id)
    total_result = await db.execute(count_query)
    total = len(total_result.unique().all())
    
    query = (
        select(LikedSong)
        .where(LikedSong.user_id == current_user_id)
        .options(selectinload(LikedSong.track))
        .order_by(LikedSong.added_at.desc())
        .offset(offset)
        .limit(size)
    )
    result = await db.execute(query)
    liked_songs = result.scalars().unique().all()
    
    items = [TrackResponse.model_validate(ls.track) for ls in liked_songs if ls.track]
    pages = (total + size - 1) // size
    return Page[TrackResponse](
        items=items,
        total=total,
        page=page,
        size=size,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1,
    )

@router.post("/liked-songs/{track_id}")
async def like_track(
    track_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    # Ensure track exists first
    track_query = select(Track).where(Track.id == track_id)
    track_result = await db.execute(track_query)
    if not track_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Track not found in local DB. Fetch it first.")
        
    query = select(LikedSong).where(LikedSong.user_id == current_user_id, LikedSong.track_id == track_id)
    result = await db.execute(query)
    if result.scalar_one_or_none():
        return {"status": "ok"}
        
    ls = LikedSong(user_id=current_user_id, track_id=track_id)
    db.add(ls)
    await db.commit()
    return {"status": "ok"}

@router.delete("/liked-songs/{track_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unlike_track(
    track_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    query = select(LikedSong).where(LikedSong.user_id == current_user_id, LikedSong.track_id == track_id)
    result = await db.execute(query)
    ls = result.scalar_one_or_none()
    if ls:
        await db.delete(ls)
        await db.commit()

@router.get("/albums", response_model=Page[AlbumResponse])
async def get_saved_albums(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    offset = (page - 1) * size
    
    count_query = select(SavedAlbum).where(SavedAlbum.user_id == current_user_id)
    total_result = await db.execute(count_query)
    total = len(total_result.unique().all())
    
    query = (
        select(SavedAlbum)
        .where(SavedAlbum.user_id == current_user_id)
        .options(selectinload(SavedAlbum.album))
        .order_by(SavedAlbum.added_at.desc())
        .offset(offset)
        .limit(size)
    )
    result = await db.execute(query)
    saved_albums = result.scalars().unique().all()
    
    items = [AlbumResponse.model_validate(sa.album) for sa in saved_albums if sa.album]
    pages = (total + size - 1) // size
    return Page[AlbumResponse](
        items=items,
        total=total,
        page=page,
        size=size,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1,
    )

@router.post("/albums/{album_id}")
async def save_album(
    album_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    album_query = select(Album).where(Album.id == album_id)
    album_result = await db.execute(album_query)
    if not album_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Album not found in local DB. Fetch it first.")
        
    query = select(SavedAlbum).where(SavedAlbum.user_id == current_user_id, SavedAlbum.album_id == album_id)
    result = await db.execute(query)
    if result.scalar_one_or_none():
        return {"status": "ok"}
        
    sa = SavedAlbum(user_id=current_user_id, album_id=album_id)
    db.add(sa)
    await db.commit()
    return {"status": "ok"}

@router.delete("/albums/{album_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unsave_album(
    album_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    query = select(SavedAlbum).where(SavedAlbum.user_id == current_user_id, SavedAlbum.album_id == album_id)
    result = await db.execute(query)
    sa = result.scalar_one_or_none()
    if sa:
        await db.delete(sa)
        await db.commit()

@router.get("/history", response_model=Page[TrackResponse])
async def get_play_history(
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    offset = (page - 1) * size
    
    count_query = select(PlayHistory).where(PlayHistory.user_id == current_user_id)
    total_result = await db.execute(count_query)
    total = len(total_result.unique().all())
    
    query = (
        select(PlayHistory)
        .where(PlayHistory.user_id == current_user_id)
        .options(selectinload(PlayHistory.track))
        .order_by(PlayHistory.played_at.desc())
        .offset(offset)
        .limit(size)
    )
    result = await db.execute(query)
    history_entries = result.scalars().unique().all()
    
    items = [TrackResponse.model_validate(h.track) for h in history_entries if h.track]
    pages = (total + size - 1) // size
    return Page[TrackResponse](
        items=items,
        total=total,
        page=page,
        size=size,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1,
    )

@router.post("/history/{track_id}")
async def add_play_history(
    track_id: str,
    db: AsyncSession = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id),
):
    track_query = select(Track).where(Track.id == track_id)
    track_result = await db.execute(track_query)
    if not track_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Track not found in local DB. Fetch it first.")
        
    ph = PlayHistory(user_id=current_user_id, track_id=track_id)
    db.add(ph)
    await db.commit()
    return {"status": "ok"}
