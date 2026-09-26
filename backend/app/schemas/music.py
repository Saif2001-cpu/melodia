from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class TrackBase(BaseModel):
    id: str
    title: str
    artist_name: str
    artist_id: str
    album_title: Optional[str] = None
    album_id: Optional[str] = None
    duration_ms: int
    preview_url: Optional[str] = None
    cover_url: Optional[str] = None
    explicit: bool = False
    rank: Optional[int] = None
    genres: List[str] = []

    model_config = ConfigDict(from_attributes=True)

class TrackResponse(TrackBase):
    pass

class AlbumBase(BaseModel):
    id: str
    title: str
    artist_name: str
    artist_id: str
    cover_url: Optional[str] = None
    release_date: Optional[str] = None
    # The ORM model stores this as 'total_tracks'; provider dataclass uses 'track_count'.
    # We expose it as 'track_count' (matching the frontend) and accept both field names.
    track_count: Optional[int] = None
    genres: List[str] = []
    tracks: List[TrackResponse] = []

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    @classmethod
    def model_validate(cls, obj, **kwargs):
        # Coerce ORM Album (which has total_tracks) to track_count
        if hasattr(obj, 'total_tracks') and not hasattr(obj, 'track_count'):
            data = {c.key: getattr(obj, c.key) for c in obj.__table__.columns}
            data['track_count'] = data.pop('total_tracks', None)
            return cls(**data)
        return super().model_validate(obj, **kwargs)

class AlbumResponse(AlbumBase):
    pass

class ArtistBase(BaseModel):
    id: str
    name: str
    picture_url: Optional[str] = None
    fan_count: int = 0
    genres: List[str] = []
    top_tracks: List[TrackResponse] = []
    albums: List[AlbumBase] = []

    model_config = ConfigDict(from_attributes=True)

class ArtistResponse(ArtistBase):
    pass
