"""Redis connection pool and helper."""

from typing import Any

import redis.asyncio as aioredis

from app.core.config import get_settings

settings = get_settings()

_redis_pool: aioredis.Redis | None = None  # type: ignore[type-arg]


async def get_redis() -> aioredis.Redis:  # type: ignore[type-arg]
    """Return the shared Redis connection pool (lazy init)."""
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = aioredis.from_url(
            str(settings.REDIS_URL),
            encoding="utf-8",
            decode_responses=True,
        )
    return _redis_pool


async def close_redis() -> None:
    global _redis_pool
    if _redis_pool is not None:
        await _redis_pool.aclose()
        _redis_pool = None


class CacheClient:
    """Thin wrapper around redis with namespaced keys and TTL defaults."""

    def __init__(self, namespace: str = "melodia") -> None:
        self._ns = namespace

    def _key(self, key: str) -> str:
        return f"{self._ns}:{key}"

    async def get(self, key: str) -> Any:
        r = await get_redis()
        return await r.get(self._key(key))

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        r = await get_redis()
        effective_ttl = ttl if ttl is not None else settings.CACHE_TTL_SECONDS
        await r.set(self._key(key), value, ex=effective_ttl)

    async def delete(self, key: str) -> None:
        r = await get_redis()
        await r.delete(self._key(key))

    async def delete_pattern(self, pattern: str) -> None:
        r = await get_redis()
        keys = await r.keys(self._key(pattern))
        if keys:
            await r.delete(*keys)

    async def exists(self, key: str) -> bool:
        r = await get_redis()
        return bool(await r.exists(self._key(key)))
