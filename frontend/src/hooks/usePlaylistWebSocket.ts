import { useEffect, useRef } from 'react'
import { useQueryClient } from '@tanstack/react-query'

export function usePlaylistWebSocket(playlistId: string | undefined) {
  const queryClient = useQueryClient()
  const ws = useRef<WebSocket | null>(null)

  useEffect(() => {
    if (!playlistId) return

    // Construct WebSocket URL based on current origin
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${protocol}//${window.location.host}/api/v1/playlists/${playlistId}/ws`

    ws.current = new WebSocket(wsUrl)

    ws.current.onopen = () => {
      console.log(`Connected to playlist ${playlistId} websocket`)
    }

    ws.current.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        if (data.event === 'track_added' || data.event === 'track_removed' || data.event === 'tracks_reordered') {
          // Invalidate the playlist query so it refetches immediately
          queryClient.invalidateQueries({ queryKey: ['playlist', playlistId] })
        }
      } catch (err) {
        console.error('Error parsing websocket message', err)
      }
    }

    ws.current.onclose = () => {
      console.log(`Disconnected from playlist ${playlistId} websocket`)
    }

    return () => {
      if (ws.current) {
        ws.current.close()
      }
    }
  }, [playlistId, queryClient])
}
