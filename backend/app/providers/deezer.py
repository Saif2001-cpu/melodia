"""Deezer public API music provider implementation.

Deezer's public REST API requires no API key for read-only metadata and
30-second track previews. Docs: https://developers.deezer.com/api
"""

import json

import httpx
import structlog

from app.core.config import get_settings
from app.core.exceptions import ExternalServiceError, NotFoundError
from app.providers.base import (
    AlbumData,
    ArtistData,
    MusicProvider,
    SearchResults,
    TrackData,
)

logger = structlog.get_logger(__name__)
settings = get_settings()


def _safe_cover(obj: dict, key: str = "cover_medium") -> str | None:
    return obj.get(key) or obj.get("cover") or obj.get("picture_medium") or obj.get("picture")


def _parse_track(raw: dict) -> TrackData:
    artist = raw.get("artist") or {}
    album = raw.get("album") or {}
    return TrackData(
        id=str(raw["id"]),
        title=raw.get("title", "Unknown"),
        artist_name=artist.get("name", "Unknown"),
        artist_id=str(artist.get("id", "")),
        album_title=album.get("title", "Unknown"),
        album_id=str(album.get("id", "")),
        duration_ms=raw.get("duration", 0) * 1000,
        preview_url=raw.get("preview"),
        cover_url=_safe_cover(album),
        explicit=bool(raw.get("explicit_lyrics", False)),
        rank=raw.get("rank", 0),
    )


def _parse_album(raw: dict) -> AlbumData:
    artist = raw.get("artist") or {}
    tracks_data = raw.get("tracks", {}).get("data", [])
    return AlbumData(
        id=str(raw["id"]),
        title=raw.get("title", "Unknown"),
        artist_name=artist.get("name", "Unknown"),
        artist_id=str(artist.get("id", "")),
        cover_url=_safe_cover(raw),
        release_date=raw.get("release_date"),
        track_count=raw.get("nb_tracks", len(tracks_data)),
        genres=[g["name"] for g in raw.get("genres", {}).get("data", [])],
        tracks=[_parse_track({**t, "album": raw}) for t in tracks_data],
    )


def _parse_artist(raw: dict) -> ArtistData:
    return ArtistData(
        id=str(raw["id"]),
        name=raw.get("name", "Unknown"),
        picture_url=_safe_cover(raw, "picture_medium"),
        fan_count=raw.get("nb_fan", 0),
    )


class DeezerProvider(MusicProvider):
    """Music provider backed by Deezer's public REST API."""

    def __init__(self) -> None:
        self._base = str(settings.DEEZER_API_BASE_URL).rstrip("/")
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self._base,
                timeout=httpx.Timeout(10.0),
                headers={"Accept": "application/json"},
            )
        return self._client

    async def _request(self, path: str, params: dict | None = None) -> dict:
        client = await self._get_client()
        try:
            resp = await client.get(path, params=params)
            resp.raise_for_status()
            data = resp.json()
        except httpx.HTTPStatusError as exc:
            raise ExternalServiceError("Deezer", str(exc)) from exc
        except (httpx.RequestError, json.JSONDecodeError) as exc:
            raise ExternalServiceError("Deezer", str(exc)) from exc

        if "error" in data:
            err = data["error"]
            if isinstance(err, dict) and err.get("code") == 800:
                raise NotFoundError("Resource")
            raise ExternalServiceError("Deezer", str(err))
        return data  # type: ignore[return-value]

    async def search(
        self,
        query: str,
        *,
        limit: int = 20,
        offset: int = 0,
    ) -> SearchResults:
        track_data = await self._request("/search", {"q": query, "limit": limit, "index": offset})
        album_data = await self._request(
            "/search/album", {"q": query, "limit": limit, "index": offset}
        )
        artist_data = await self._request(
            "/search/artist", {"q": query, "limit": limit, "index": offset}
        )
        return SearchResults(
            tracks=[_parse_track(t) for t in track_data.get("data", [])],
            albums=[_parse_album(a) for a in album_data.get("data", [])],
            artists=[_parse_artist(a) for a in artist_data.get("data", [])],
            total_tracks=track_data.get("total", 0),
            total_albums=album_data.get("total", 0),
            total_artists=artist_data.get("total", 0),
        )

    async def get_track(self, track_id: str) -> TrackData:
        data = await self._request(f"/track/{track_id}")
        return _parse_track(data)

    async def get_album(self, album_id: str) -> AlbumData:
        data = await self._request(f"/album/{album_id}")
        return _parse_album(data)

    async def get_artist(self, artist_id: str) -> ArtistData:
        raw = await self._request(f"/artist/{artist_id}")
        artist = _parse_artist(raw)
        try:
            top_raw = await self._request(f"/artist/{artist_id}/top", {"limit": 10})
            artist.top_tracks = [_parse_track(t) for t in top_raw.get("data", [])]
        except Exception:
            logger.warning("Could not fetch top tracks", artist_id=artist_id)
        try:
            albums_raw = await self._request(f"/artist/{artist_id}/albums", {"limit": 20})
            artist.albums = [_parse_album(a) for a in albums_raw.get("data", [])]
        except Exception:
            logger.warning("Could not fetch albums", artist_id=artist_id)
        return artist

    async def get_trending(self, *, limit: int = 20) -> list[TrackData]:
        data = await self._request("/chart/0/tracks", {"limit": limit})
        return [_parse_track(t) for t in data.get("data", [])]

    async def get_artist_top_tracks(self, artist_id: str, *, limit: int = 10) -> list[TrackData]:
        data = await self._request(f"/artist/{artist_id}/top", {"limit": limit})
        return [_parse_track(t) for t in data.get("data", [])]

    async def get_tracks_by_genre(self, genre: str, *, limit: int = 20) -> list[TrackData]:
        data = await self._request("/search", {"q": genre, "limit": limit})
        return [_parse_track(t) for t in data.get("data", [])]

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()
