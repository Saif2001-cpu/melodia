# Melodia — Architecture

## Overview

Melodia is a full-stack music streaming web application with a Python/FastAPI backend and React/TypeScript frontend.

```
┌──────────────────────────────────────────────────────────────────────┐
│                            Browser / Client                           │
│                  React + TypeScript + Vite + Tailwind                 │
│          TanStack Query (server state) │ Zustand (client state)       │
└────────────────────────────┬─────────────────────────────────────────┘
                             │ HTTP/REST + WebSocket
┌────────────────────────────▼─────────────────────────────────────────┐
│                         FastAPI Backend                               │
│  /api/v1/{auth,search,music,albums,artists,playlists,library,history,│
│            recommendations,ws}                                        │
│                                                                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │  Routes  │→ │ Services │→ │ Repositories │→ │     Models      │  │
│  └──────────┘  └─────┬────┘  └──────────────┘  └────────┬────────┘  │
│                      │  ┌───────────────────────────────┘            │
│                      ▼  ▼                                             │
│  ┌──────────────────────────────────────────────────────────────┐    │
│  │              MusicProvider (abstract)                        │    │
│  │  DeezerProvider │ MockMusicProvider │ [Future: ML Provider]  │    │
│  └──────────────────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────────────────┘
         │                                │
┌────────▼────────┐              ┌────────▼────────┐
│   PostgreSQL    │              │      Redis       │
│  (persistent)   │              │  (cache/pubsub)  │
└─────────────────┘              └─────────────────┘
```

## Backend Layer Architecture

| Layer        | Location             | Responsibility                                      |
|-------------|----------------------|-----------------------------------------------------|
| Routes      | `api/v1/endpoints/`  | HTTP request parsing, response serialization        |
| Schemas     | `schemas/`           | Pydantic request/response models                    |
| Services    | `services/`          | Business logic, orchestration                       |
| Repositories| `repositories/`      | Database queries (SQLAlchemy async)                 |
| Models      | `models/`            | SQLAlchemy ORM models                               |
| Providers   | `providers/`         | External music API abstraction                      |
| Core        | `core/`              | Config, security, exceptions, logging, deps         |
| DB          | `db/`                | Session factory, Redis client                       |

## Data Flow

```
Request → Route (validate) → Service (business logic)
        → Repository (DB query) → Model → Response Schema → JSON
        → Provider (external API, cached in Redis)
```

## Music Provider Abstraction

```python
class MusicProvider(ABC):
    async def search(query, *, limit, offset) -> SearchResults
    async def get_track(track_id) -> TrackData
    async def get_album(album_id) -> AlbumData
    async def get_artist(artist_id) -> ArtistData
    async def get_trending(*, limit) -> list[TrackData]
    async def get_artist_top_tracks(artist_id, *, limit) -> list[TrackData]
    async def get_tracks_by_genre(genre, *, limit) -> list[TrackData]
```

**Implementations:**
- `DeezerProvider` — Deezer public REST API (no key required, 30s previews)
- `MockMusicProvider` — deterministic in-memory data for tests
- *(Future)* `SpotifyProvider`, `JamendoProvider`, or ML-augmented provider

## Database Schema (Phase 2)

Key tables:
- `users` — auth, profile
- `tracks` — cached track metadata
- `albums` — cached album metadata
- `artists` — cached artist metadata
- `playlists` — user playlists
- `playlist_tracks` — ordered playlist–track join
- `liked_songs` — user–track likes
- `saved_albums` — user–album saves
- `followed_artists` — user–artist follows
- `play_history` — listening history
- `playlist_collaborators` — collaborative playlist members

## Caching Strategy

| Data            | TTL      | Key pattern                   |
|-----------------|----------|-------------------------------|
| Trending tracks | 10 min   | `melodia:trending:{limit}`    |
| Track metadata  | 24 hours | `melodia:track:{id}`          |
| Album metadata  | 24 hours | `melodia:album:{id}`          |
| Artist metadata | 24 hours | `melodia:artist:{id}`         |
| Search results  | 5 min    | `melodia:search:{q}:{offset}` |
| User library    | 1 min    | `melodia:user:{id}:library`   |

## Real-time (Phase 9)

WebSocket endpoint: `ws://api/v1/ws/playlists/{playlist_id}`

Events:
- `track_added` — broadcast when a collaborator adds a track
- `track_removed` — broadcast on removal
- `track_reordered` — broadcast on reorder
- `collaborator_joined` / `collaborator_left`

## API Endpoints

```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
POST   /api/v1/auth/refresh
GET    /api/v1/auth/me

GET    /api/v1/search?q=...
GET    /api/v1/music/trending
GET    /api/v1/music/tracks/{id}
GET    /api/v1/albums/{id}
GET    /api/v1/artists/{id}
GET    /api/v1/artists/{id}/top-tracks

GET    /api/v1/playlists
POST   /api/v1/playlists
GET    /api/v1/playlists/{id}
PATCH  /api/v1/playlists/{id}
DELETE /api/v1/playlists/{id}
POST   /api/v1/playlists/{id}/tracks
DELETE /api/v1/playlists/{id}/tracks/{track_id}
PATCH  /api/v1/playlists/{id}/tracks/{track_id}

GET    /api/v1/library/liked-songs
POST   /api/v1/library/liked-songs/{track_id}
DELETE /api/v1/library/liked-songs/{track_id}
GET    /api/v1/library/albums
POST   /api/v1/library/albums/{album_id}
DELETE /api/v1/library/albums/{album_id}
GET    /api/v1/library/artists
POST   /api/v1/library/artists/{artist_id}
DELETE /api/v1/library/artists/{artist_id}

GET    /api/v1/history/recent
GET    /api/v1/recommendations

WS     /api/v1/ws/playlists/{playlist_id}
```

## Frontend Architecture

```
src/
├── api/           # Axios modules per domain (auth, music, playlists, library)
├── components/    # Reusable UI (common, player, sidebar, cards, modals)
├── hooks/         # Custom hooks wrapping TanStack Query
├── layouts/       # MainLayout, AuthLayout
├── pages/         # Route-level page components
├── store/         # Zustand stores (authStore, playerStore)
├── types/         # Shared TypeScript interfaces
└── utils/         # Formatting helpers, constants
```

## Build Phases

| Phase | Focus                        | Status       |
|-------|------------------------------|-------------|
| 1     | Architecture + setup          | ✅ Complete |
| 2     | Database + migrations         | ✅ Complete |
| 3     | Authentication                | ✅ Complete |
| 4     | Music API integration         | 🔜 Next     |
| 5     | React UI                      | Pending     |
| 6     | Music player + queue          | Pending     |
| 7     | Playlists + library           | Pending     |
| 8     | Recommendations               | Pending     |
| 9     | WebSockets + collaborative    | Pending     |
| 10    | Testing + Docker + CI/CD      | Pending     |
