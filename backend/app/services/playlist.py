"""Playlist business logic (CRUD, track management, permissions).

Kept separate from the API layer so route handlers stay thin and
authorization rules live in one place.
"""

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import ForbiddenError, NotFoundError
from app.models.playlist import Playlist, PlaylistTrack
from app.models.track import Track
from app.models.user import User
from app.repositories.base import BaseRepository


class PlaylistRepository(BaseRepository[Playlist]):
    """Repository for Playlist model with eager-loading helpers."""

    async def get_for_user(
        self, session: AsyncSession, *, playlist_id: str, load_tracks: bool = True
    ) -> Playlist:
        """Get a playlist (with owner, optionally tracks+tracks' track).

        Raises :class:`NotFoundError` if it does not exist.
        """
        query = (
            select(Playlist)
            .where(Playlist.id == playlist_id)
            .options(selectinload(Playlist.owner))
        )
        if load_tracks:
            query = query.options(
                selectinload(Playlist.tracks).selectinload(PlaylistTrack.track)
            )
        result = await session.execute(query)
        playlist = result.scalar_one_or_none()
        if playlist is None:
            raise NotFoundError("Playlist", identifier=playlist_id)
        return playlist

    async def list_for_owner(
        self, session: AsyncSession, *, owner_id: str, offset: int, limit: int
    ) -> list[Playlist]:
        result = await session.execute(
            select(Playlist)
            .where(Playlist.owner_id == owner_id)
            .options(
                selectinload(Playlist.owner),
                selectinload(Playlist.tracks).selectinload(PlaylistTrack.track),
            )
            .order_by(Playlist.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(result.scalars().unique().all())

    async def count_for_owner(self, session: AsyncSession, *, owner_id: str) -> int:
        return (
            await session.execute(
                select(func.count()).select_from(Playlist).where(Playlist.owner_id == owner_id)
            )
        ).scalar_one()


playlist_repo = PlaylistRepository(Playlist)  # type: ignore[arg-type]


class PlaylistService:
    """Service layer for playlists."""

    # ── Authorization ────────────────────────────────────────────────────────

    @staticmethod
    def check_view_access(playlist: Playlist, user_id: str) -> None:
        if not playlist.is_public and playlist.owner_id != user_id:
            raise ForbiddenError("Not authorized to view this playlist")

    @staticmethod
    def check_modify_access(playlist: Playlist, user_id: str) -> None:
        """Owner always allowed; collaborative playlists allow any authed user."""
        if playlist.owner_id != user_id and not playlist.is_collaborative:
            raise ForbiddenError("Not authorized to modify this playlist")

    @staticmethod
    def check_owner_access(playlist: Playlist, user_id: str) -> None:
        if playlist.owner_id != user_id:
            raise ForbiddenError("Only the playlist owner can perform this action")

    # ── CRUD ─────────────────────────────────────────────────────────────────

    async def create_playlist(
        self,
        session: AsyncSession,
        *,
        user_id: str,
        name: str,
        description: str | None,
        is_public: bool,
        is_collaborative: bool,
    ) -> Playlist:
        user = await session.get(User, user_id)
        if user is None:
            raise NotFoundError("User", identifier=user_id)

        playlist = Playlist(
            name=name,
            description=description,
            is_public=is_public,
            is_collaborative=is_collaborative,
            owner_id=user_id,
        )
        session.add(playlist)
        await session.commit()
        await session.refresh(playlist)
        return playlist

    async def delete_playlist(self, session: AsyncSession, *, playlist_id: str, user_id: str) -> None:
        playlist = await playlist_repo.get_for_user(
            session, playlist_id=playlist_id, load_tracks=False
        )
        self.check_owner_access(playlist, user_id)
        await session.delete(playlist)
        await session.commit()

    # ── Tracks ───────────────────────────────────────────────────────────────

    async def add_track(
        self, session: AsyncSession, *, playlist_id: str, track_id: str, user_id: str
    ) -> None:
        """Add a track to a playlist. Idempotent. Raises NotFoundError if the
        track isn't cached locally yet."""
        playlist = await playlist_repo.get_for_user(session, playlist_id=playlist_id)
        self.check_modify_access(playlist, user_id)

        track = await session.get(Track, track_id)
        if track is None:
            raise NotFoundError("Track", identifier=track_id)

        if any(pt.track_id == track_id for pt in playlist.tracks):
            return  # already present — no-op

        session.add(
            PlaylistTrack(
                playlist_id=playlist_id,
                track_id=track_id,
                position=len(playlist.tracks),
                added_by_id=user_id,
            )
        )
        await session.commit()

    async def remove_track(
        self, session: AsyncSession, *, playlist_id: str, track_id: str, user_id: str
    ) -> None:
        playlist = await playlist_repo.get_for_user(
            session, playlist_id=playlist_id, load_tracks=False
        )
        self.check_modify_access(playlist, user_id)

        result = await session.execute(
            select(PlaylistTrack).where(
                PlaylistTrack.playlist_id == playlist_id,
                PlaylistTrack.track_id == track_id,
            )
        )
        pt = result.scalar_one_or_none()
        if pt is None:
            return

        await session.delete(pt)
        # Close the gap left by the removed track so positions stay contiguous.
        subsequent = await session.execute(
            select(PlaylistTrack).where(
                PlaylistTrack.playlist_id == playlist_id,
                PlaylistTrack.position > pt.position,
            )
        )
        for sub_pt in subsequent.scalars().all():
            sub_pt.position -= 1
        await session.commit()

    async def reorder_tracks(
        self, session: AsyncSession, *, playlist_id: str, track_ids: list[str], user_id: str
    ) -> None:
        playlist = await playlist_repo.get_for_user(session, playlist_id=playlist_id)
        self.check_modify_access(playlist, user_id)

        pt_map = {pt.track_id: pt for pt in playlist.tracks}
        for i, tid in enumerate(track_ids):
            if tid in pt_map:
                pt_map[tid].position = i
        await session.commit()


playlist_service = PlaylistService()
