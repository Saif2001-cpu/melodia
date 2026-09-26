"""Abstract Music Provider interface + shared data types."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class TrackData:
    id: str
    title: str
    artist_name: str
    artist_id: str
    album_title: str
    album_id: str
    duration_ms: int
    preview_url: str | None
    cover_url: str | None
    explicit: bool = False
    rank: int = 0
    genres: list[str] = field(default_factory=list)


@dataclass
class AlbumData:
    id: str
    title: str
    artist_name: str
    artist_id: str
    cover_url: str | None
    release_date: str | None
    track_count: int
    genres: list[str] = field(default_factory=list)
    tracks: list[TrackData] = field(default_factory=list)


@dataclass
class ArtistData:
    id: str
    name: str
    picture_url: str | None
    fan_count: int = 0
    genres: list[str] = field(default_factory=list)
    top_tracks: list[TrackData] = field(default_factory=list)
    albums: list[AlbumData] = field(default_factory=list)


@dataclass
class SearchResults:
    tracks: list[TrackData]
    albums: list[AlbumData]
    artists: list[ArtistData]
    total_tracks: int = 0
    total_albums: int = 0
    total_artists: int = 0


class MusicProvider(ABC):
    """Abstract base class for music metadata/preview providers."""

    @abstractmethod
    async def search(
        self,
        query: str,
        *,
        limit: int = 20,
        offset: int = 0,
    ) -> SearchResults:
        """Full-text search across tracks, albums, and artists."""

    @abstractmethod
    async def get_track(self, track_id: str) -> TrackData:
        """Fetch a single track by its provider ID."""

    @abstractmethod
    async def get_album(self, album_id: str) -> AlbumData:
        """Fetch an album with its tracks."""

    @abstractmethod
    async def get_artist(self, artist_id: str) -> ArtistData:
        """Fetch an artist with top tracks and albums."""

    @abstractmethod
    async def get_trending(self, *, limit: int = 20) -> list[TrackData]:
        """Return trending/chart tracks."""

    @abstractmethod
    async def get_artist_top_tracks(self, artist_id: str, *, limit: int = 10) -> list[TrackData]:
        """Return an artist's top tracks."""

    @abstractmethod
    async def get_tracks_by_genre(self, genre: str, *, limit: int = 20) -> list[TrackData]:
        """Return tracks for a given genre."""
