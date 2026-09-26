"""Unit tests for the music providers."""

import pytest

from app.providers.mock import MockMusicProvider


@pytest.mark.asyncio
class TestMockMusicProvider:
    """Tests for MockMusicProvider — validates provider contract."""

    async def test_search_returns_results(self):
        provider = MockMusicProvider()
        results = await provider.search("neon")
        assert len(results.tracks) > 0
        assert results.tracks[0].title is not None

    async def test_search_no_match_returns_empty(self):
        provider = MockMusicProvider()
        results = await provider.search("zzznomatch999")
        assert results.tracks == []
        assert results.albums == []
        assert results.artists == []

    async def test_get_track_success(self):
        provider = MockMusicProvider()
        track = await provider.get_track("t1")
        assert track.id == "t1"
        assert track.title == "Neon Pulse"
        assert track.duration_ms > 0

    async def test_get_track_not_found(self):
        from app.core.exceptions import NotFoundError

        provider = MockMusicProvider()
        with pytest.raises(NotFoundError):
            await provider.get_track("does-not-exist")

    async def test_get_album_success(self):
        provider = MockMusicProvider()
        album = await provider.get_album("al1")
        assert album.id == "al1"
        assert len(album.tracks) > 0

    async def test_get_artist_success(self):
        provider = MockMusicProvider()
        artist = await provider.get_artist("a1")
        assert artist.id == "a1"
        assert len(artist.top_tracks) > 0

    async def test_get_trending(self):
        provider = MockMusicProvider()
        tracks = await provider.get_trending(limit=2)
        assert len(tracks) <= 2

    async def test_get_artist_top_tracks(self):
        provider = MockMusicProvider()
        tracks = await provider.get_artist_top_tracks("a1")
        assert all(t.artist_id == "a1" for t in tracks)
