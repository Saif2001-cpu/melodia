from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from app.schemas.music import TrackResponse

class PlaylistTrackResponse(BaseModel):
    position: int
    added_at: datetime
    track: TrackResponse
    
    model_config = ConfigDict(from_attributes=True)

class PlaylistBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = False
    is_collaborative: bool = False

class PlaylistCreate(PlaylistBase):
    pass

class PlaylistUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None
    is_collaborative: Optional[bool] = None

class PlaylistResponse(PlaylistBase):
    id: str
    cover_url: Optional[str] = None
    owner_id: str
    owner_name: str = "" # We'll populate this
    track_count: int = 0
    created_at: datetime
    updated_at: datetime
    tracks: List[PlaylistTrackResponse] = []
    
    model_config = ConfigDict(from_attributes=True)
