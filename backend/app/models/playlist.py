"""Playlist models."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base import TimestampMixin, generate_uuid

if TYPE_CHECKING:
    from app.models.track import Track
    from app.models.user import User


class Playlist(Base, TimestampMixin):
    __tablename__ = "playlists"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    cover_url: Mapped[str | None] = mapped_column(String, nullable=True)
    owner_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    is_public: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_collaborative: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="playlists")
    tracks: Mapped[list["PlaylistTrack"]] = relationship(
        "PlaylistTrack",
        back_populates="playlist",
        cascade="all, delete-orphan",
        order_by="PlaylistTrack.position",
    )
    collaborators: Mapped[list["PlaylistCollaborator"]] = relationship(
        "PlaylistCollaborator", back_populates="playlist", cascade="all, delete-orphan"
    )


class PlaylistTrack(Base):
    __tablename__ = "playlist_tracks"

    playlist_id: Mapped[str] = mapped_column(
        ForeignKey("playlists.id", ondelete="CASCADE"), primary_key=True
    )
    track_id: Mapped[str] = mapped_column(
        ForeignKey("tracks.id", ondelete="CASCADE"), primary_key=True
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    added_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        nullable=False,
    )
    added_by_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    playlist: Mapped["Playlist"] = relationship("Playlist", back_populates="tracks")
    track: Mapped["Track"] = relationship("Track")
    added_by: Mapped["User"] = relationship("User")


class PlaylistCollaborator(Base):
    __tablename__ = "playlist_collaborators"

    playlist_id: Mapped[str] = mapped_column(
        ForeignKey("playlists.id", ondelete="CASCADE"), primary_key=True
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
        nullable=False,
    )

    playlist: Mapped["Playlist"] = relationship("Playlist", back_populates="collaborators")
    user: Mapped["User"] = relationship("User")
