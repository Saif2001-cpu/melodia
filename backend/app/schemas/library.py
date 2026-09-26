from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from app.schemas.playlist import PlaylistResponse
from app.schemas.music import AlbumResponse, ArtistResponse

class LibraryItem(BaseModel):
    type: str # 'playlist', 'album', 'artist'
    playlist: Optional[PlaylistResponse] = None
    album: Optional[AlbumResponse] = None
    artist: Optional[ArtistResponse] = None
    saved_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
