"""Top-level API v1 router — assembles all endpoint routers."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, music, playlists, library

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(music.router, prefix="/music", tags=["music"])
api_router.include_router(playlists.router, prefix="/playlists", tags=["playlists"])
api_router.include_router(library.router, prefix="/library", tags=["library"])

# Routers will be imported and included as phases progress
# Phase 5+: history, recommendations


# Placeholder health sub-route so router is never empty
@api_router.get("/ping", tags=["health"])
async def ping() -> dict[str, str]:
    return {"pong": "true"}
