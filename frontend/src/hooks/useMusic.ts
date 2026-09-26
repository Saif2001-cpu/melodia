import { useQuery } from '@tanstack/react-query'
import { musicApi } from '@/api/music'
import { extractApiError } from '@/api/client'

export const musicKeys = {
  all: ['music'] as const,
  search: (query: string, limit?: number, offset?: number) =>
    [...musicKeys.all, 'search', query, limit, offset] as const,
  trending: (limit?: number) => [...musicKeys.all, 'trending', limit] as const,
  track: (id: string) => [...musicKeys.all, 'track', id] as const,
  album: (id: string) => [...musicKeys.all, 'album', id] as const,
  artist: (id: string) => [...musicKeys.all, 'artist', id] as const,
  recommendations: (limit?: number) => [...musicKeys.all, 'recommendations', limit] as const,
}

export function useSearch(query: string, limit = 20, offset = 0) {
  return useQuery({
    queryKey: musicKeys.search(query, limit, offset),
    queryFn: async () => {
      try {
        return await musicApi.search(query, { limit, offset })
      } catch (err) {
        throw new Error(extractApiError(err))
      }
    },
    enabled: !!query,
    staleTime: 1000 * 60 * 5, // 5 minutes
  })
}

export function useTrending(limit = 20) {
  return useQuery({
    queryKey: musicKeys.trending(limit),
    queryFn: async () => {
      try {
        return await musicApi.getTrending(limit)
      } catch (err) {
        throw new Error(extractApiError(err))
      }
    },
    staleTime: 1000 * 60 * 60, // 1 hour
  })
}

export function useRecommendations(limit = 20) {
  return useQuery({
    queryKey: musicKeys.recommendations(limit),
    queryFn: async () => {
      try {
        return await musicApi.getRecommendations(limit)
      } catch (err) {
        throw new Error(extractApiError(err))
      }
    },
    staleTime: 1000 * 60 * 15, // 15 mins
  })
}

export function useTrack(id: string) {
  return useQuery({
    queryKey: musicKeys.track(id),
    queryFn: async () => {
      try {
        return await musicApi.getTrack(id)
      } catch (err) {
        throw new Error(extractApiError(err))
      }
    },
    enabled: !!id,
    staleTime: 1000 * 60 * 60 * 24, // 24 hours
  })
}

export function useAlbum(id: string) {
  return useQuery({
    queryKey: musicKeys.album(id),
    queryFn: async () => {
      try {
        return await musicApi.getAlbum(id)
      } catch (err) {
        throw new Error(extractApiError(err))
      }
    },
    enabled: !!id,
    staleTime: 1000 * 60 * 60 * 24, // 24 hours
  })
}

export function useArtist(id: string) {
  return useQuery({
    queryKey: musicKeys.artist(id),
    queryFn: async () => {
      try {
        return await musicApi.getArtist(id)
      } catch (err) {
        throw new Error(extractApiError(err))
      }
    },
    enabled: !!id,
    staleTime: 1000 * 60 * 60 * 24, // 24 hours
  })
}
