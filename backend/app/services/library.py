"""Library business logic (liked songs, saved albums, play history).

Encapsulates all database access for the library feature so that API
endpoints stay thin and the same logic can be reused by other services.
"""

from collections.abc import Callable, Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import NotFoundError
from app.models.library import FollowedArtist, LikedSong, PlayHistory, SavedAlbum
from app.models.track import Album, Artist, Track
from app.schemas.pagination import Page


def build_page[T](items: list[T], *, total: int, page: int, size: int) -> Page[T]:
    """Assemble a :class:`Page` envelope from a fetched slice + total count."""
    pages = max(1, -(-total // size)) if total else 0
    return Page[T](
        items=items,
        total=total,
        page=page,
        size=size,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1,
    )


async def paginate(
    session: AsyncSession,
    model,
    *,
    user_id: str,
    loader_options: Sequence[Callable] = (),
    order_by,
    page: int,
    size: int,
) -> tuple[list, int]:
    """Return one page of a user's rows of ``model`` plus the total count.

    Uses a scalar COUNT query instead of loading every row just to count it.
    """
    total = (
        await session.execute(
            select(func.count()).select_from(model).where(model.user_id == user_id)
        )
    ).scalar_one()

    query = (
        select(model)
        .where(model.user_id == user_id)
        .options(*loader_options)
        .order_by(order_by)
        .offset((page - 1) * size)
        .limit(size)
    )
    result = await session.execute(query)
    return list(result.scalars().unique().all()), total


class LibraryService:
    """Service layer for the user's personal music library."""

    # ── Liked songs ──────────────────────────────────────────────────────────

    async def get_liked_songs(
        self, session: AsyncSession, *, user_id: str, page: int, size: int
    ) -> tuple[list[Track], int]:
        rows, total = await paginate(
            session,
            LikedSong,
            user_id=user_id,
            loader_options=[selectinload(LikedSong.track)],
            order_by=LikedSong.added_at.desc(),
            page=page,
            size=size,
        )
        return [row.track for row in rows if row.track], total

    async def like_track(self, session: AsyncSession, *, user_id: str, track_id: str) -> None:
        """Like a track, ensuring it exists locally first. Idempotent."""
        await self._require(session, Track, track_id, "Track")
        existing = await session.execute(
            select(LikedSong).where(
                LikedSong.user_id == user_id, LikedSong.track_id == track_id
            )
        )
        if existing.scalar_one_or_none() is None:
            session.add(LikedSong(user_id=user_id, track_id=track_id))
            await session.commit()

    async def unlike_track(self, session: AsyncSession, *, user_id: str, track_id: str) -> None:
        result = await session.execute(
            select(LikedSong).where(
                LikedSong.user_id == user_id, LikedSong.track_id == track_id
            )
        )
        liked = result.scalar_one_or_none()
        if liked:
            await session.delete(liked)
            await session.commit()

    # ── Saved albums ─────────────────────────────────────────────────────────

    async def get_saved_albums(
        self, session: AsyncSession, *, user_id: str, page: int, size: int
    ) -> tuple[list[Album], int]:
        rows, total = await paginate(
            session,
            SavedAlbum,
            user_id=user_id,
            loader_options=[selectinload(SavedAlbum.album)],
            order_by=SavedAlbum.added_at.desc(),
            page=page,
            size=size,
        )
        return [row.album for row in rows if row.album], total

    async def save_album(self, session: AsyncSession, *, user_id: str, album_id: str) -> None:
        """Save an album, ensuring it exists locally first. Idempotent."""
        await self._require(session, Album, album_id, "Album")
        existing = await session.execute(
            select(SavedAlbum).where(
                SavedAlbum.user_id == user_id, SavedAlbum.album_id == album_id
            )
        )
        if existing.scalar_one_or_none() is None:
            session.add(SavedAlbum(user_id=user_id, album_id=album_id))
            await session.commit()

    async def unsave_album(self, session: AsyncSession, *, user_id: str, album_id: str) -> None:
        result = await session.execute(
            select(SavedAlbum).where(
                SavedAlbum.user_id == user_id, SavedAlbum.album_id == album_id
            )
        )
        saved = result.scalar_one_or_none()
        if saved:
            await session.delete(saved)
            await session.commit()

    # ── Followed artists ─────────────────────────────────────────────────────

    async def get_followed_artists(
        self, session: AsyncSession, *, user_id: str, page: int, size: int
    ) -> tuple[list[Artist], int]:
        rows, total = await paginate(
            session,
            FollowedArtist,
            user_id=user_id,
            loader_options=[selectinload(FollowedArtist.artist)],
            order_by=FollowedArtist.added_at.desc(),
            page=page,
            size=size,
        )
        return [row.artist for row in rows if row.artist], total

    async def follow_artist(self, session: AsyncSession, *, user_id: str, artist_id: str) -> None:
        """Follow an artist, ensuring it exists locally first. Idempotent."""
        await self._require(session, Artist, artist_id, "Artist")
        existing = await session.execute(
            select(FollowedArtist).where(
                FollowedArtist.user_id == user_id, FollowedArtist.artist_id == artist_id
            )
        )
        if existing.scalar_one_or_none() is None:
            session.add(FollowedArtist(user_id=user_id, artist_id=artist_id))
            await session.commit()

    async def unfollow_artist(self, session: AsyncSession, *, user_id: str, artist_id: str) -> None:
        result = await session.execute(
            select(FollowedArtist).where(
                FollowedArtist.user_id == user_id, FollowedArtist.artist_id == artist_id
            )
        )
        followed = result.scalar_one_or_none()
        if followed:
            await session.delete(followed)
            await session.commit()

    # ── Play history ─────────────────────────────────────────────────────────

    async def get_play_history(
        self, session: AsyncSession, *, user_id: str, page: int, size: int
    ) -> tuple[list[Track], int]:
        rows, total = await paginate(
            session,
            PlayHistory,
            user_id=user_id,
            loader_options=[selectinload(PlayHistory.track)],
            order_by=PlayHistory.played_at.desc(),
            page=page,
            size=size,
        )
        return [row.track for row in rows if row.track], total

    async def add_play_history(self, session: AsyncSession, *, user_id: str, track_id: str) -> None:
        await self._require(session, Track, track_id, "Track")
        session.add(PlayHistory(user_id=user_id, track_id=track_id))
        await session.commit()

    async def get_last_played_track(self, session: AsyncSession, *, user_id: str) -> Track | None:
        """Most recently played track for a user, used for recommendations."""
        result = await session.execute(
            select(PlayHistory)
            .where(PlayHistory.user_id == user_id)
            .options(selectinload(PlayHistory.track))
            .order_by(PlayHistory.played_at.desc())
            .limit(1)
        )
        entry = result.scalar_one_or_none()
        return entry.track if entry else None

    # ── Helpers ──────────────────────────────────────────────────────────────

    @staticmethod
    async def _require(
        session: AsyncSession, model, obj_id: str, resource: str
    ) -> None:
        """Raise :class:`NotFoundError` unless ``obj_id`` exists in ``model``."""
        result = await session.execute(select(model).where(model.id == obj_id))
        if result.scalars().first() is None:
            raise NotFoundError(resource, identifier=None)


library_service = LibraryService()
