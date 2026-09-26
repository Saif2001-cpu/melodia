import { describe, it, expect } from 'vitest'
import { usePlayerStore } from '@/store/playerStore'
import type { Track } from '@/types'

const mockTrack: Track = {
  id: 't1',
  title: 'Neon Pulse',
  artist_name: 'Synth Wave',
  artist_id: 'a1',
  album_title: 'Electric Dreams',
  album_id: 'al1',
  duration_ms: 210000,
  preview_url: null,
  cover_url: null,
  explicit: false,
  rank: 950000,
  genres: ['Electronic'],
}

describe('playerStore', () => {
  it('sets current track when setTrack is called', () => {
    const store = usePlayerStore.getState()
    store.setTrack(mockTrack)
    expect(usePlayerStore.getState().currentTrack).toEqual(mockTrack)
    expect(usePlayerStore.getState().isPlaying).toBe(true)
  })

  it('toggles play state', () => {
    usePlayerStore.getState().pause()
    expect(usePlayerStore.getState().isPlaying).toBe(false)
    usePlayerStore.getState().togglePlay()
    expect(usePlayerStore.getState().isPlaying).toBe(true)
  })

  it('cycles repeat modes', () => {
    const store = usePlayerStore.getState()
    // Reset
    usePlayerStore.setState({ repeatMode: 'off' })
    store.cycleRepeat()
    expect(usePlayerStore.getState().repeatMode).toBe('queue')
    store.cycleRepeat()
    expect(usePlayerStore.getState().repeatMode).toBe('track')
    store.cycleRepeat()
    expect(usePlayerStore.getState().repeatMode).toBe('off')
  })

  it('clamps volume between 0 and 1', () => {
    usePlayerStore.getState().setVolume(2)
    expect(usePlayerStore.getState().volume).toBe(1)
    usePlayerStore.getState().setVolume(-1)
    expect(usePlayerStore.getState().volume).toBe(0)
  })

  it('adds tracks to queue', () => {
    usePlayerStore.setState({ queue: [mockTrack] })
    const anotherTrack = { ...mockTrack, id: 't2', title: 'Another Track' }
    usePlayerStore.getState().addToQueue(anotherTrack)
    expect(usePlayerStore.getState().queue).toHaveLength(2)
  })
})
