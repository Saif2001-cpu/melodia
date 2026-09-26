# Melodia 🎵

A production-quality music streaming web application. Discover, play, and organize the music you love.

> **Note:** This project uses the [Deezer public API](https://developers.deezer.com/api) for music metadata and 30-second track previews. No Spotify assets, branding, or source code is used.

## Tech Stack

| Layer      | Technology                                          |
|-----------|-----------------------------------------------------|
| Frontend  | React 18 + TypeScript + Vite + Tailwind CSS         |
| State     | TanStack Query (server) + Zustand (client)          |
| Routing   | React Router v6                                     |
| Backend   | Python 3.11 + FastAPI + Pydantic v2                 |
| ORM       | SQLAlchemy 2 (async) + Alembic                      |
| Database  | PostgreSQL 16                                        |
| Cache     | Redis 7                                             |
| Auth      | JWT (HS256) + bcrypt                                |
| Real-time | WebSockets                                          |
| Testing   | Pytest + Vitest + Testing Library                   |
| Infra     | Docker + Docker Compose + GitHub Actions            |

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for local frontend dev)
- Python 3.11+ (for local backend dev)

### 1. Clone and configure

```bash
git clone <repo>
cd melodia

cp .env.example .env
# Edit .env — at minimum change SECRET_KEY
```

### 2. Start with Docker Compose

```bash
docker compose up -d
```

Services:
- **Frontend** → http://localhost:5173
- **Backend API** → http://localhost:8000
- **API Docs** → http://localhost:8000/api/docs
- **PostgreSQL** → localhost:5432
- **Redis** → localhost:6379

### 3. Run database migrations

```bash
docker compose exec backend alembic upgrade head
```

### Local Development (without Docker)

**Backend:**
```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## Running Tests

**Backend:**
```bash
cd backend
poetry run pytest tests/ -v
poetry run ruff check .
poetry run mypy app/
```

**Frontend:**
```bash
cd frontend
npm test
npm run type-check
npm run lint
```

## Project Structure

```
melodia/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/   # Route handlers
│   │   ├── core/               # Config, security, exceptions, deps
│   │   ├── db/                 # SQLAlchemy session, Redis client
│   │   ├── models/             # ORM models
│   │   ├── providers/          # Music API abstraction (Deezer, Mock)
│   │   ├── repositories/       # DB queries
│   │   ├── schemas/            # Pydantic schemas
│   │   ├── services/           # Business logic
│   │   └── main.py             # FastAPI app factory
│   ├── alembic/                # Database migrations
│   └── tests/                  # Backend tests
├── frontend/
│   └── src/
│       ├── api/                # Axios API modules
│       ├── components/         # Reusable UI components
│       ├── hooks/              # TanStack Query hooks
│       ├── layouts/            # Page layouts
│       ├── pages/              # Route page components
│       ├── store/              # Zustand stores
│       └── types/              # TypeScript types
├── docs/
│   └── ARCHITECTURE.md
├── .github/workflows/ci.yml
├── docker-compose.yml
└── .env.example
```

## Environment Variables

See [`.env.example`](.env.example) for all variables with documentation.

Key variables:
| Variable      | Description                      | Required |
|--------------|----------------------------------|---------|
| `SECRET_KEY` | JWT signing key (min 32 chars)   | ✅ Yes   |
| `DATABASE_URL`| PostgreSQL connection string     | ✅ Yes   |
| `REDIS_URL`  | Redis connection string          | ✅ Yes   |
| `MUSIC_PROVIDER` | `deezer` or `mock`           | No       |

## API Documentation

Swagger UI: http://localhost:8000/api/docs (development only)

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for full API endpoint listing.

## Contributing

1. Branch from `develop`
2. Write tests for new features
3. Run lint/type-check before PR
4. CI must pass

## License

MIT
