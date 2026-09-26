"""Provider factory — resolves the configured music provider."""

from functools import lru_cache

from app.core.config import get_settings
from app.providers.base import MusicProvider


@lru_cache(maxsize=1)
def get_music_provider() -> MusicProvider:
    settings = get_settings()
    if settings.MUSIC_PROVIDER == "deezer":
        from app.providers.deezer import DeezerProvider

        return DeezerProvider()
    if settings.MUSIC_PROVIDER == "mock":
        from app.providers.mock import MockMusicProvider

        return MockMusicProvider()
    raise ValueError(f"Unknown music provider: {settings.MUSIC_PROVIDER}")
