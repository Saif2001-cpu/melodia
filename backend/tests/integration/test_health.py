"""Integration test for the health endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient):
    resp = await client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert "version" in body


@pytest.mark.asyncio
async def test_api_ping(client: AsyncClient):
    resp = await client.get("/api/v1/ping")
    assert resp.status_code == 200
    assert resp.json()["pong"] == "true"
