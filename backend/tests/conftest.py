"""conftest.py — shared pytest fixtures."""

import asyncio
import os
from collections.abc import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

# ─────────────────────────────────────────────────────────────────────────────
# Set environment variables BEFORE importing any app modules so that
# pydantic-settings doesn't try to validate real PostgreSQL / Redis URLs.
# ─────────────────────────────────────────────────────────────────────────────
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://melodia:melodia@localhost:5432/melodia")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("SECRET_KEY", "test-secret-key-32-chars-long-padding!!")
os.environ.setdefault("MUSIC_PROVIDER", "mock")
os.environ.setdefault("ENVIRONMENT", "development")

# ─────────────────────────────────────────────────────────────────────────────
# Late imports — after env vars are in place
# ─────────────────────────────────────────────────────────────────────────────
from app.db.session import Base, get_db  # noqa: E402
from app.main import create_app  # noqa: E402
from app.providers.factory import get_music_provider  # noqa: E402
from app.providers.mock import MockMusicProvider  # noqa: E402

# In-memory SQLite for fast unit tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine():  # type: ignore[no-untyped-def]
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:  # type: ignore[no-untyped-def]
    session_factory = async_sessionmaker(test_engine, expire_on_commit=False)
    async with session_factory() as session:
        yield session
        await session.rollback()


@pytest.fixture
def mock_provider() -> MockMusicProvider:
    return MockMusicProvider()


@pytest_asyncio.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator:  # type: ignore[type-arg]
    """Async HTTPX test client with DB and provider overrides."""
    from httpx import ASGITransport, AsyncClient

    app = create_app()

    async def override_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_music_provider] = lambda: MockMusicProvider()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
