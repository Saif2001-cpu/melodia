import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { playlistApi } from '@/api/playlists'
import type { CreatePlaylistRequest, UpdatePlaylistRequest } from '@/types'

export function usePlaylists(page = 1, size = 20) {
  return useQuery({
    queryKey: ['playlists', page, size],
    queryFn: () => playlistApi.getPlaylists(page, size),
  })
}

export function usePlaylist(id: string) {
  return useQuery({
    queryKey: ['playlist', id],
    queryFn: () => playlistApi.getPlaylist(id),
    enabled: !!id,
  })
}

export function useCreatePlaylist() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: CreatePlaylistRequest) => playlistApi.createPlaylist(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['playlists'] })
    },
  })
}

export function useUpdatePlaylist() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: UpdatePlaylistRequest }) =>
      playlistApi.updatePlaylist(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['playlists'] })
      queryClient.invalidateQueries({ queryKey: ['playlist', variables.id] })
    },
  })
}

export function useDeletePlaylist() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: playlistApi.deletePlaylist,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['playlists'] })
    },
  })
}

export function useAddTrackToPlaylist() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ playlistId, trackId }: { playlistId: string; trackId: string }) =>
      playlistApi.addTrack(playlistId, trackId),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['playlist', variables.playlistId] })
    },
  })
}

export function useRemoveTrackFromPlaylist() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ playlistId, trackId }: { playlistId: string; trackId: string }) =>
      playlistApi.removeTrack(playlistId, trackId),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['playlist', variables.playlistId] })
    },
  })
}
