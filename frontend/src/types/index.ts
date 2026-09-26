// ── User ──────────────────────────────────────────────────────────────────────
export interface User {
  id: string
  email: string
  username: string
  is_active: boolean
  is_superuser: boolean
  created_at: string
}

// ── Auth ──────────────────────────────────────────────────────────────────────
export interface AuthTokens {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  username: string
  password: string
}

// ── Track ─────────────────────────────────────────────────────────────────────
export interface Track {
  id: string
  title: string
  artist_name: string
  artist_id: string
  album_title?: string | null
  album_id?: string | null
  duration_ms: number
  preview_url: string | null
  cover_url: string | null
  explicit: boolean
  rank?: number | null
  genres: string[]
  is_liked?: boolean
}

// ── Album ─────────────────────────────────────────────────────────────────────
export interface Album {
  id: string
  title: string
  artist_name: string
  artist_id: string
  cover_url: string | null
  release_date: string | null
  track_count: number
  genres: string[]
  tracks: Track[]
  is_saved?: boolean
}

// ── Artist ────────────────────────────────────────────────────────────────────
export interface Artist {
  id: string
  name: string
  picture_url: string | null
  fan_count: number
  genres: string[]
  top_tracks: Track[]
  albums: Album[]
  is_followed?: boolean
}

// ── Search ────────────────────────────────────────────────────────────────────
export interface SearchResults {
  tracks: Track[]
  albums: Album[]
  artists: Artist[]
  total_tracks: number
  total_albums: number
  total_artists: number
}

// ── Playlist ──────────────────────────────────────────────────────────────────
export interface Playlist {
  id: string
  name: string
  description: string | null
  cover_url: string | null
  is_public: boolean
  is_collaborative: boolean
  owner_id: string
  owner_name: string
  track_count: number
  tracks: PlaylistTrack[]
  followers?: number
  created_at: string
  updated_at: string
}

export interface PlaylistTrack {
  position: number
  added_at: string
  track: Track
}

export interface CreatePlaylistRequest {
  name: string
  description?: string
  is_public?: boolean
  is_collaborative?: boolean
}

export interface UpdatePlaylistRequest {
  name?: string
  description?: string
  is_public?: boolean
  is_collaborative?: boolean
}

// ── Library ───────────────────────────────────────────────────────────────────
export interface LibraryItem {
  type: 'playlist' | 'album' | 'artist'
  playlist?: Playlist
  album?: Album
  artist?: Artist
  saved_at: string
}

// ── Player Queue ──────────────────────────────────────────────────────────────
export type RepeatMode = 'off' | 'track' | 'queue'

export interface PlayerState {
  currentTrack: Track | null
  queue: Track[]
  queueIndex: number
  isPlaying: boolean
  isShuffle: boolean
  repeatMode: RepeatMode
  volume: number
  progress: number
  duration: number
}

// ── Pagination ────────────────────────────────────────────────────────────────
export interface Page<T> {
  items: T[]
  total: number
  page: number
  size: number
  pages: number
  has_next: boolean
  has_prev: boolean
}

// ── API Error ─────────────────────────────────────────────────────────────────
export interface ApiError {
  error: string
  message: string
  detail?: unknown
}
