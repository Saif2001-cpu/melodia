"""Mock music provider for tests — no network calls."""

from app.providers.base import (
    AlbumData,
    ArtistData,
    MusicProvider,
    SearchResults,
    TrackData,
)

_MOCK_TRACKS = [
    TrackData(
        id="t1",
        title="Neon Pulse",
        artist_name="Synth Wave",
        artist_id="a1",
        album_title="Electric Dreams",
        album_id="al1",
        duration_ms=210000,
        preview_url="https://example.com/previews/neon_pulse.mp3",
        cover_url="https://picsum.photos/seed/t1/300",
        explicit=False,
        rank=950000,
    ),
    TrackData(
        id="t2",
        title="Midnight Drive",
        artist_name="Synth Wave",
        artist_id="a1",
        album_title="Electric Dreams",
        album_id="al1",
        duration_ms=195000,
        preview_url="https://example.com/previews/midnight_drive.mp3",
        cover_url="https://picsum.photos/seed/t2/300",
        explicit=False,
        rank=870000,
    ),
    TrackData(
        id="t3",
        title="Solar Flare",
        artist_name="Cosmic Beat",
        artist_id="a2",
        album_title="Orbit",
        album_id="al2",
        duration_ms=240000,
        preview_url="https://example.com/previews/solar_flare.mp3",
        cover_url="https://picsum.photos/seed/t3/300",
        explicit=True,
        rank=760000,
    ),
]

_MOCK_ALBUMS = [
    AlbumData(
        id="al1",
        title="Electric Dreams",
        artist_name="Synth Wave",
        artist_id="a1",
        cover_url="https://picsum.photos/seed/al1/300",
        release_date="2024-03-15",
        track_count=2,
        genres=["Electronic", "Synthwave"],
        tracks=_MOCK_TRACKS[:2],
    ),
    AlbumData(
        id="al2",
        title="Orbit",
        artist_name="Cosmic Beat",
        artist_id="a2",
        cover_url="https://picsum.photos/seed/al2/300",
        release_date="2023-11-20",
        track_count=1,
        genres=["Electronic"],
        tracks=_MOCK_TRACKS[2:],
    ),
]

_MOCK_ARTISTS = [
    ArtistData(
        id="a1",
        name="Synth Wave",
        picture_url="https://picsum.photos/seed/a1/300",
        fan_count=125000,
        genres=["Electronic", "Synthwave"],
        top_tracks=_MOCK_TRACKS[:2],
        albums=_MOCK_ALBUMS[:1],
    ),
    ArtistData(
        id="a2",
        name="Cosmic Beat",
        picture_url="https://picsum.photos/seed/a2/300",
        fan_count=89000,
        genres=["Electronic"],
        top_tracks=_MOCK_TRACKS[2:],
        albums=_MOCK_ALBUMS[1:],
    ),
]


class MockMusicProvider(MusicProvider):
    """In-memory music provider for unit/integration tests."""

    async def search(self, query: str, *, limit: int = 20, offset: int = 0) -> SearchResults:
        q = query.lower()
        tracks = [t for t in _MOCK_TRACKS if q in t.title.lower() or q in t.artist_name.lower()]
        albums = [a for a in _MOCK_ALBUMS if q in a.title.lower()]
        artists = [a for a in _MOCK_ARTISTS if q in a.name.lower()]
        return SearchResults(
            tracks=tracks[offset : offset + limit],
            albums=albums[offset : offset + limit],
            artists=artists[offset : offset + limit],
            total_tracks=len(tracks),
            total_albums=len(albums),
            total_artists=len(artists),
        )

    async def get_track(self, track_id: str) -> TrackData:
        from app.core.exceptions import NotFoundError

        for t in _MOCK_TRACKS:
            if t.id == track_id:
                return t
        raise NotFoundError("Track", track_id)

    async def get_album(self, album_id: str) -> AlbumData:
        from app.core.exceptions import NotFoundError

        for a in _MOCK_ALBUMS:
            if a.id == album_id:
                return a
        raise NotFoundError("Album", album_id)

    async def get_artist(self, artist_id: str) -> ArtistData:
        from app.core.exceptions import NotFoundError

        for a in _MOCK_ARTISTS:
            if a.id == artist_id:
                return a
        raise NotFoundError("Artist", artist_id)

    async def get_trending(self, *, limit: int = 20) -> list[TrackData]:
        return _MOCK_TRACKS[:limit]

    async def get_artist_top_tracks(self, artist_id: str, *, limit: int = 10) -> list[TrackData]:
        return [t for t in _MOCK_TRACKS if t.artist_id == artist_id][:limit]

    async def get_tracks_by_genre(self, genre: str, *, limit: int = 20) -> list[TrackData]:
        return _MOCK_TRACKS[:limit]
