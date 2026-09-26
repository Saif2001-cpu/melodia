import { create } from 'zustand'
import type { Track, RepeatMode, PlayerState } from '@/types'
import { seekAudio } from '@/hooks/useAudioPlayer'

interface PlayerStore extends PlayerState {
  // Actions
  setTrack: (track: Track, queue?: Track[]) => void
  playQueue: (queue: Track[], startIndex?: number) => void
  togglePlay: () => void
  play: () => void
  pause: () => void
  next: () => void
  previous: () => void
  seek: (progress: number) => void
  setVolume: (volume: number) => void
  toggleShuffle: () => void
  cycleRepeat: () => void
  addToQueue: (track: Track) => void
  removeFromQueue: (index: number) => void
  setProgress: (progress: number) => void
  setDuration: (duration: number) => void
}

export const usePlayerStore = create<PlayerStore>((set, get) => ({
  // Initial state
  currentTrack: null,
  queue: [],
  queueIndex: 0,
  isPlaying: false,
  isShuffle: false,
  repeatMode: 'off',
  volume: 0.8,
  progress: 0,
  duration: 0,

  setTrack: (track, queue) => {
    const newQueue = queue ?? [track]
    const idx = newQueue.indexOf(track)
    set({ currentTrack: track, queue: newQueue, queueIndex: idx >= 0 ? idx : 0, isPlaying: true, progress: 0 })
  },

  playQueue: (queue, startIndex = 0) => {
    if (!queue.length) return
    set({
      queue,
      queueIndex: startIndex,
      currentTrack: queue[startIndex],
      isPlaying: true,
      progress: 0,
    })
  },

  togglePlay: () => set((s) => ({ isPlaying: !s.isPlaying })),
  play: () => set({ isPlaying: true }),
  pause: () => set({ isPlaying: false }),

  next: () => {
    const { queue, queueIndex, isShuffle, repeatMode } = get()
    if (!queue.length) return

    let nextIdx: number
    if (repeatMode === 'track') {
      nextIdx = queueIndex
    } else if (isShuffle) {
      nextIdx = Math.floor(Math.random() * queue.length)
    } else {
      nextIdx = queueIndex + 1
      if (nextIdx >= queue.length) {
        nextIdx = repeatMode === 'queue' ? 0 : queueIndex
      }
    }
    set({ queueIndex: nextIdx, currentTrack: queue[nextIdx], progress: 0, isPlaying: true })
  },

  previous: () => {
    const { queue, queueIndex, progress } = get()
    if (!queue.length) return
    // If more than 3s in, restart from beginning
    if (progress > 3) {
      seekAudio(0)
      set({ progress: 0 })
      return
    }
    const prevIdx = Math.max(0, queueIndex - 1)
    set({ queueIndex: prevIdx, currentTrack: queue[prevIdx], progress: 0, isPlaying: true })
  },

  seek: (progress) => set({ progress }),
  setProgress: (progress) => set({ progress }),
  setDuration: (duration) => set({ duration }),
  setVolume: (volume) => set({ volume: Math.max(0, Math.min(1, volume)) }),
  toggleShuffle: () => set((s) => ({ isShuffle: !s.isShuffle })),

  cycleRepeat: () =>
    set((s) => {
      const modes: RepeatMode[] = ['off', 'queue', 'track']
      const next = modes[(modes.indexOf(s.repeatMode) + 1) % modes.length]
      return { repeatMode: next }
    }),

  addToQueue: (track) =>
    set((s) => ({ queue: [...s.queue, track] })),

  removeFromQueue: (index) =>
    set((s) => {
      const queue = s.queue.filter((_, i) => i !== index)
      const queueIndex = index < s.queueIndex ? s.queueIndex - 1 : s.queueIndex
      return { queue, queueIndex }
    }),
}))
