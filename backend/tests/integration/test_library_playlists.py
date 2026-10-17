"""Integration tests for the library and playlist endpoints."""

import pytest
from httpx import AsyncClient

PREFIX = "/api/v1"


@pytest.fixture
def track_payload():
    """A valid TrackData payload (as returned by the mock provider)."""
    return {
        "id": "t1",
        "title": "Neon Pulse",
        "artist_name": "Volt Rider",
        "artist_id": "a1",
        "album_title": "Circuit Dreams",
        "album_id": "al1",
        "duration_ms": 180_000,
        "preview_url": None,
        "cover_url": None,
        "explicit": False,
        "rank": 1,
        "genres": [],
    }


async def _seed_track(client: AsyncClient, headers: dict, payload: dict) -> None:
    """Cache a track locally via the provider-backed search flow substitute.

    The music endpoints don't persist tracks, so tests insert directly via
    the history endpoint after seeding through SQLAlchemy is not possible
    over HTTP; instead we exploit that play-history validates existence —
    so we seed using the DB session fixture in the tests that need it.
    """
    raise NotImplementedError


class TestLikedSongs:
    async def test_requires_auth(self, client: AsyncClient):
        resp = await client.get(f"{PREFIX}/library/liked-songs")
        assert resp.status_code == 403

    async def test_empty_list(self, client: AsyncClient, auth_headers):
        resp = await client.get(f"{PREFIX}/library/liked-songs", headers=auth_headers)
        assert resp.status_code == 200
        body = resp.json()
        assert body["items"] == []
        assert body["total"] == 0

    async def test_like_unknown_track_returns_404(self, client: AsyncClient, auth_headers):
        resp = await client.post(f"{PREFIX}/library/liked-songs/nope", headers=auth_headers)
        assert resp.status_code == 404
        assert "not found" in resp.json()["message"].lower()


class TestFollowedArtists:
    async def test_follow_and_list(self, client: AsyncClient, auth_headers, artist):
        resp = await client.post(
            f"{PREFIX}/library/artists/{artist.id}", headers=auth_headers
        )
        assert resp.status_code == 200

        # idempotent second follow
        resp = await client.post(
            f"{PREFIX}/library/artists/{artist.id}", headers=auth_headers
        )
        assert resp.status_code == 200

        resp = await client.get(f"{PREFIX}/library/artists", headers=auth_headers)
        assert resp.status_code == 200
        body = resp.json()
        assert body["total"] == 1
        assert body["items"][0]["id"] == artist.id

        resp = await client.delete(
            f"{PREFIX}/library/artists/{artist.id}", headers=auth_headers
        )
        assert resp.status_code == 204

        resp = await client.get(f"{PREFIX}/library/artists", headers=auth_headers)
        assert resp.json()["total"] == 0


class TestPlayHistory:
    async def test_add_history_unknown_track_404(self, client: AsyncClient, auth_headers):
        resp = await client.post(f"{PREFIX}/library/history/missing", headers=auth_headers)
        assert resp.status_code == 404


class TestPlaylists:
    async def test_create_list_get_delete(
        self, client: AsyncClient, auth_headers, user
    ):
        resp = await client.post(
            f"{PREFIX}/playlists",
            headers=auth_headers,
            json={"name": "Road Trip", "description": "bangers", "is_public": True},
        )
        assert resp.status_code == 201
        pl = resp.json()
        assert pl["name"] == "Road Trip"
        assert pl["owner_name"] == user.username
        assert pl["track_count"] == 0

        resp = await client.get(f"{PREFIX}/playlists", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["total"] == 1

        resp = await client.get(f"{PREFIX}/playlists/{pl['id']}", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["name"] == "Road Trip"

        resp = await client.delete(f"{PREFIX}/playlists/{pl['id']}", headers=auth_headers)
        assert resp.status_code == 204

        resp = await client.get(f"{PREFIX}/playlists/{pl['id']}", headers=auth_headers)
        assert resp.status_code == 404

    async def test_add_track_validated_body(self, client: AsyncClient, auth_headers):
        resp = await client.post(
            f"{PREFIX}/playlists", headers=auth_headers, json={"name": "Empty"}
        )
        pid = resp.json()["id"]

        # missing track_id → 422 (typed request model)
        resp = await client.post(f"{PREFIX}/playlists/{pid}/tracks", headers=auth_headers, json={})
        assert resp.status_code == 422

        # unknown track → 404
        resp = await client.post(
            f"{PREFIX}/playlists/{pid}/tracks",
            headers=auth_headers,
            json={"track_id": "nope"},
        )
        assert resp.status_code == 404

    async def test_private_playlist_not_visible_to_others(
        self, client: AsyncClient, db_session, user
    ):
        from app.core.security import create_access_token
        from app.models.playlist import Playlist

        other_token = {"Authorization": f"Bearer {create_access_token('other-user')}"}
        resp = await client.post(
            f"{PREFIX}/playlists", headers=auth_headers, json={"name": "Secret"}
        )
        pid = resp.json()["id"]

        resp = await client.get(f"{PREFIX}/playlists/{pid}", headers=other_token)
        assert resp.status_code == 403
