"""Application configuration using pydantic-settings."""

from functools import lru_cache
from typing import Literal

from pydantic import AnyHttpUrl, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── App ──────────────────────────────────────────────────────────────────
    APP_NAME: str = "Melodia"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = False

    # ── API ──────────────────────────────────────────────────────────────────
    API_V1_PREFIX: str = "/api/v1"
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    # ── Database ─────────────────────────────────────────────────────────────
    DATABASE_URL: PostgresDsn = PostgresDsn(
        "postgresql+asyncpg://melodia:melodia@localhost:5432/melodia"
    )
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_ECHO: bool = False

    # ── Redis ────────────────────────────────────────────────────────────────
    REDIS_URL: RedisDsn = RedisDsn("redis://localhost:6379/0")
    CACHE_TTL_SECONDS: int = 300  # 5 minutes default

    # ── Auth / JWT ────────────────────────────────────────────────────────────
    SECRET_KEY: str = "change-me-in-production-at-least-32-chars-long"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── Music provider ────────────────────────────────────────────────────────
    MUSIC_PROVIDER: Literal["deezer", "mock"] = "deezer"
    # Deezer uses a public API — no key required for basic endpoints
    DEEZER_API_BASE_URL: AnyHttpUrl = AnyHttpUrl("https://api.deezer.com")

    # ── Pagination ────────────────────────────────────────────────────────────
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # ── Logging ──────────────────────────────────────────────────────────────
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: Literal["json", "console"] = "console"

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def parse_origins(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def async_database_url(self) -> str:
        return str(self.DATABASE_URL)


@lru_cache
def get_settings() -> Settings:
    return Settings()
