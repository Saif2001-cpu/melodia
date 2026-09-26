import { apiClient } from './client'
import type { Album, Artist, Page, Track } from '@/types'

export const libraryApi = {
  // ── Liked songs ───────────────────────────────────────────────────────────
  getLikedSongs: async (page = 1, size = 50): Promise<Page<Track>> => {
    const resp = await apiClient.get<Page<Track>>('/library/liked-songs', {
      params: { page, size },
    })
    return resp.data
  },

  likeTrack: async (trackId: string): Promise<void> => {
    await apiClient.post(`/library/liked-songs/${trackId}`)
  },

  unlikeTrack: async (trackId: string): Promise<void> => {
    await apiClient.delete(`/library/liked-songs/${trackId}`)
  },

  // ── Saved albums ──────────────────────────────────────────────────────────
  getSavedAlbums: async (page = 1, size = 20): Promise<Page<Album>> => {
    const resp = await apiClient.get<Page<Album>>('/library/albums', { params: { page, size } })
    return resp.data
  },

  saveAlbum: async (albumId: string): Promise<void> => {
    await apiClient.post(`/library/albums/${albumId}`)
  },

  unsaveAlbum: async (albumId: string): Promise<void> => {
    await apiClient.delete(`/library/albums/${albumId}`)
  },

  // ── Followed artists ──────────────────────────────────────────────────────
  getFollowedArtists: async (page = 1, size = 20): Promise<Page<Artist>> => {
    const resp = await apiClient.get<Page<Artist>>('/library/artists', {
      params: { page, size },
    })
    return resp.data
  },

  followArtist: async (artistId: string): Promise<void> => {
    await apiClient.post(`/library/artists/${artistId}`)
  },

  unfollowArtist: async (artistId: string): Promise<void> => {
    await apiClient.delete(`/library/artists/${artistId}`)
  },

  // ── Play History ──────────────────────────────────────────────────────────
  getPlayHistory: async (page = 1, size = 50): Promise<Page<Track>> => {
    const resp = await apiClient.get<Page<Track>>('/library/history', { params: { page, size } })
    return resp.data
  },

  addPlayHistory: async (trackId: string): Promise<void> => {
    await apiClient.post(`/library/history/${trackId}`)
  },
}
