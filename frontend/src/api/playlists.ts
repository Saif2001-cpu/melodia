import { apiClient } from './client'
import type { Page, Playlist, CreatePlaylistRequest, UpdatePlaylistRequest } from '@/types'

export const playlistApi = {
  getPlaylists: async (page = 1, size = 20): Promise<Page<Playlist>> => {
    const resp = await apiClient.get<Page<Playlist>>('/playlists', { params: { page, size } })
    return resp.data
  },

  getPlaylist: async (id: string): Promise<Playlist> => {
    const resp = await apiClient.get<Playlist>(`/playlists/${id}`)
    return resp.data
  },

  createPlaylist: async (data: CreatePlaylistRequest): Promise<Playlist> => {
    const resp = await apiClient.post<Playlist>('/playlists', data)
    return resp.data
  },

  updatePlaylist: async (id: string, data: UpdatePlaylistRequest): Promise<Playlist> => {
    const resp = await apiClient.patch<Playlist>(`/playlists/${id}`, data)
    return resp.data
  },

  deletePlaylist: async (id: string): Promise<void> => {
    await apiClient.delete(`/playlists/${id}`)
  },

  addTrack: async (playlistId: string, trackId: string): Promise<void> => {
    await apiClient.post(`/playlists/${playlistId}/tracks`, { track_id: trackId })
  },

  removeTrack: async (playlistId: string, trackId: string): Promise<void> => {
    await apiClient.delete(`/playlists/${playlistId}/tracks/${trackId}`)
  },

  reorderTracks: async (
    playlistId: string,
    trackId: string,
    newPosition: number,
  ): Promise<void> => {
    await apiClient.patch(`/playlists/${playlistId}/tracks/${trackId}`, {
      position: newPosition,
    })
  },
}
