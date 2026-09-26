import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { libraryApi } from '@/api/library'

export function useLikedSongs(page = 1, size = 50) {
  return useQuery({
    queryKey: ['liked-songs', page, size],
    queryFn: () => libraryApi.getLikedSongs(page, size),
  })
}

export function useSavedAlbums(page = 1, size = 20) {
  return useQuery({
    queryKey: ['saved-albums', page, size],
    queryFn: () => libraryApi.getSavedAlbums(page, size),
  })
}

export function useFollowedArtists(page = 1, size = 20) {
  return useQuery({
    queryKey: ['followed-artists', page, size],
    queryFn: () => libraryApi.getFollowedArtists(page, size),
  })
}

export function useLikeTrack() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: libraryApi.likeTrack,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['liked-songs'] })
      queryClient.invalidateQueries({ queryKey: ['track'] })
    },
  })
}

export function useUnlikeTrack() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: libraryApi.unlikeTrack,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['liked-songs'] })
      queryClient.invalidateQueries({ queryKey: ['track'] })
    },
  })
}

export function useSaveAlbum() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: libraryApi.saveAlbum,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['saved-albums'] })
      queryClient.invalidateQueries({ queryKey: ['album'] })
    },
  })
}

export function useUnsaveAlbum() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: libraryApi.unsaveAlbum,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['saved-albums'] })
      queryClient.invalidateQueries({ queryKey: ['album'] })
    },
  })
}

export function useFollowArtist() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: libraryApi.followArtist,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['followed-artists'] })
      queryClient.invalidateQueries({ queryKey: ['artist'] })
    },
  })
}

export function useUnfollowArtist() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: libraryApi.unfollowArtist,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['followed-artists'] })
      queryClient.invalidateQueries({ queryKey: ['artist'] })
    },
  })
}

export function usePlayHistory(page = 1, size = 20) {
  return useQuery({
    queryKey: ['play-history', page, size],
    queryFn: () => libraryApi.getPlayHistory(page, size),
  })
}

export function useAddPlayHistory() {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: libraryApi.addPlayHistory,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['play-history'] })
    },
  })
}
