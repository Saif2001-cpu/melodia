"""Music metadata models (cached from provider)."""

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    pass


class Artist(Base, TimestampMixin):
    __tablename__ = "artists"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    picture_url: Mapped[str | None] = mapped_column(String, nullable=True)


class Album(Base, TimestampMixin):
    __tablename__ = "albums"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    artist_name: Mapped[str] = mapped_column(String, nullable=False)
    artist_id: Mapped[str] = mapped_column(String, nullable=False)
    cover_url: Mapped[str | None] = mapped_column(String, nullable=True)
    release_date: Mapped[str | None] = mapped_column(String, nullable=True)
    total_tracks: Mapped[int | None] = mapped_column(Integer, nullable=True)


class Track(Base, TimestampMixin):
    __tablename__ = "tracks"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    artist_name: Mapped[str] = mapped_column(String, nullable=False)
    artist_id: Mapped[str] = mapped_column(String, nullable=False)
    album_title: Mapped[str | None] = mapped_column(String, nullable=True)
    album_id: Mapped[str | None] = mapped_column(String, nullable=True)
    duration_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    preview_url: Mapped[str | None] = mapped_column(String, nullable=True)
    cover_url: Mapped[str | None] = mapped_column(String, nullable=True)
    explicit: Mapped[bool] = mapped_column(Boolean, default=False)
    rank: Mapped[int | None] = mapped_column(Integer, nullable=True)
