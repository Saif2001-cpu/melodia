import { apiClient } from './client'
import type { Album, Artist, SearchResults, Track } from '@/types'

export const musicApi = {
  // ── Search ────────────────────────────────────────────────────────────────
  search: async (
    query: string,
    params?: { limit?: number; offset?: number },
  ): Promise<SearchResults> => {
    const resp = await apiClient.get<SearchResults>('/music/search', {
      params: { q: query, ...params },
    })
    return resp.data
  },

  // ── Tracks ────────────────────────────────────────────────────────────────
  getTrack: async (id: string): Promise<Track> => {
    const resp = await apiClient.get<Track>(`/music/tracks/${id}`)
    return resp.data
  },

  getTrending: async (limit = 20): Promise<Track[]> => {
    const resp = await apiClient.get<Track[]>('/music/trending', { params: { limit } })
    return resp.data
  },

  getRecommendations: async (limit = 20): Promise<Track[]> => {
    const resp = await apiClient.get<Track[]>('/music/recommendations', { params: { limit } })
    return resp.data
  },

  // ── Albums ────────────────────────────────────────────────────────────────
  getAlbum: async (id: string): Promise<Album> => {
    const resp = await apiClient.get<Album>(`/music/albums/${id}`)
    return resp.data
  },

  // ── Artists ───────────────────────────────────────────────────────────────
  getArtist: async (id: string): Promise<Artist> => {
    const resp = await apiClient.get<Artist>(`/music/artists/${id}`)
    return resp.data
  },
}
