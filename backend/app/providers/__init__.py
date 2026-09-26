"""providers package."""

from app.providers.base import (
    AlbumData,
    ArtistData,
    MusicProvider,
    SearchResults,
    TrackData,
)
from app.providers.factory import get_music_provider

__all__ = [
    "AlbumData",
    "ArtistData",
    "MusicProvider",
    "SearchResults",
    "TrackData",
    "get_music_provider",
]
