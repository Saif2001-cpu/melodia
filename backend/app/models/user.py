"""User database model."""

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base import TimestampMixin, generate_uuid

if TYPE_CHECKING:
    from app.models.library import FollowedArtist, LikedSong, PlayHistory, SavedAlbum
    from app.models.playlist import Playlist


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    playlists: Mapped[list["Playlist"]] = relationship(
        "Playlist", back_populates="owner", cascade="all, delete-orphan"
    )
    liked_songs: Mapped[list["LikedSong"]] = relationship(
        "LikedSong", back_populates="user", cascade="all, delete-orphan"
    )
    saved_albums: Mapped[list["SavedAlbum"]] = relationship(
        "SavedAlbum", back_populates="user", cascade="all, delete-orphan"
    )
    followed_artists: Mapped[list["FollowedArtist"]] = relationship(
        "FollowedArtist", back_populates="user", cascade="all, delete-orphan"
    )
    play_history: Mapped[list["PlayHistory"]] = relationship(
        "PlayHistory", back_populates="user", cascade="all, delete-orphan"
    )
