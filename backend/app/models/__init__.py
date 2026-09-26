"""
SQLAlchemy models initialization.
Import all models here so Alembic can discover them.
"""

from app.db.session import Base
from app.models.base import TimestampMixin
from app.models.library import FollowedArtist, LikedSong, PlayHistory, SavedAlbum
from app.models.playlist import Playlist, PlaylistCollaborator, PlaylistTrack
from app.models.track import Album, Artist, Track
from app.models.user import User

__all__ = [
    "Base",
    "TimestampMixin",
    "User",
    "Track",
    "Album",
    "Artist",
    "Playlist",
    "PlaylistTrack",
    "PlaylistCollaborator",
    "LikedSong",
    "SavedAlbum",
    "FollowedArtist",
    "PlayHistory",
]
