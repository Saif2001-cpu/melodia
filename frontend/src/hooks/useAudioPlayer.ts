import { useEffect, useRef } from 'react'
import { usePlayerStore } from '@/store/playerStore'

// Module-level singleton so audio element persists across remounts
let globalAudio: HTMLAudioElement | null = null
function getAudio(): HTMLAudioElement {
  if (!globalAudio) {
    globalAudio = new Audio()
    globalAudio.preload = 'auto'
  }
  return globalAudio
}

/** Seek the global audio element to a specific time. Safe to call before mount. */
export function seekAudio(time: number): void {
  getAudio().currentTime = time
}

export function useAudioPlayer() {
  const currentTrack = usePlayerStore((s) => s.currentTrack)
  const isPlaying = usePlayerStore((s) => s.isPlaying)
  const volume = usePlayerStore((s) => s.volume)
  const setProgress = usePlayerStore((s) => s.setProgress)
  const setDuration = usePlayerStore((s) => s.setDuration)
  const next = usePlayerStore((s) => s.next)

  // Keep stable refs for callbacks to avoid re-attaching listeners
  const setProgressRef = useRef(setProgress)
  const setDurationRef = useRef(setDuration)
  const nextRef = useRef(next)
  setProgressRef.current = setProgress
  setDurationRef.current = setDuration
  nextRef.current = next

  // Attach audio event listeners once
  useEffect(() => {
    const audio = getAudio()

    const handleTimeUpdate = () => setProgressRef.current(audio.currentTime)
    const handleLoadedMetadata = () => setDurationRef.current(audio.duration)
    const handleEnded = () => nextRef.current()

    audio.addEventListener('timeupdate', handleTimeUpdate)
    audio.addEventListener('loadedmetadata', handleLoadedMetadata)
    audio.addEventListener('ended', handleEnded)

    return () => {
      audio.removeEventListener('timeupdate', handleTimeUpdate)
      audio.removeEventListener('loadedmetadata', handleLoadedMetadata)
      audio.removeEventListener('ended', handleEnded)
    }
  }, []) // Empty dep — listeners set once, refs stay current

  // Sync track source + play/pause
  useEffect(() => {
    const audio = getAudio()

    if (currentTrack?.preview_url) {
      const normalizedSrc = audio.src
        ? new URL(audio.src, window.location.href).href
        : ''
      const normalizedNew = new URL(currentTrack.preview_url, window.location.href).href

      if (normalizedSrc !== normalizedNew) {
        audio.src = currentTrack.preview_url
        audio.load()
      }

      if (isPlaying) {
        audio.play().catch(console.error)
      } else {
        audio.pause()
      }
    } else {
      audio.pause()
      audio.src = ''
    }
  }, [currentTrack, isPlaying])

  // Sync volume
  useEffect(() => {
    getAudio().volume = volume
  }, [volume])

  const handleSeek = (time: number) => {
    const audio = getAudio()
    audio.currentTime = time
    setProgress(time)
  }

  return { handleSeek }
}
