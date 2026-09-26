import { useEffect, useRef } from 'react'
import { Play, Pause, SkipBack, SkipForward, Volume2, VolumeX, Repeat, Shuffle } from 'lucide-react'
import { usePlayerStore } from '@/store/playerStore'
import { useAudioPlayer } from '@/hooks/useAudioPlayer'
import { useAddPlayHistory } from '@/hooks/useLibrary'
import { cn } from '@/utils/cn'

function formatTime(seconds: number) {
  if (isNaN(seconds)) return '0:00'
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

export function Player() {
  const { currentTrack, isPlaying, togglePlay, next, previous, progress, duration, volume, setVolume, isShuffle, toggleShuffle, repeatMode, cycleRepeat } = usePlayerStore()
  
  const { handleSeek } = useAudioPlayer()
  const addHistory = useAddPlayHistory()
  // Keep stable ref to mutate to avoid re-triggering the effect
  const addHistoryRef = useRef(addHistory.mutate)
  addHistoryRef.current = addHistory.mutate

  // Track play history — only re-run when the track ID changes
  useEffect(() => {
    if (currentTrack?.id) {
      addHistoryRef.current(currentTrack.id)
    }
  }, [currentTrack?.id])

  if (!currentTrack) {
    return (
      <div className="h-24 w-full bg-surface-950/90 backdrop-blur-2xl border-t border-white/5 px-6 flex items-center justify-between relative z-30">
        <div className="text-surface-400 text-sm">Select a track to start listening...</div>
      </div>
    )
  }

  const handleProgressChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const time = Number(e.target.value)
    handleSeek(time)
  }

  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setVolume(Number(e.target.value))
  }

  const toggleMute = () => {
    setVolume(volume === 0 ? 0.8 : 0)
  }

  return (
    <div className="h-24 w-full bg-surface-950/90 backdrop-blur-2xl border-t border-white/5 px-6 flex items-center justify-between relative z-30">
      {/* Track Info */}
      <div className="w-1/3 flex items-center gap-4">
        {currentTrack.cover_url ? (
          <img src={currentTrack.cover_url} alt={currentTrack.title} className="w-14 h-14 rounded-md shadow-md object-cover" />
        ) : (
          <div className="w-14 h-14 rounded-md bg-surface-800 shadow-md" />
        )}
        <div className="flex flex-col min-w-0">
          <span className="text-white font-medium truncate hover:underline cursor-pointer">{currentTrack.title}</span>
          <span className="text-surface-400 text-xs truncate hover:underline cursor-pointer">{currentTrack.artist_name}</span>
        </div>
      </div>

      {/* Controls */}
      <div className="w-1/3 flex flex-col items-center gap-2">
        <div className="flex items-center gap-6">
          <button 
            onClick={toggleShuffle}
            className={cn("transition-colors", isShuffle ? "text-primary-400" : "text-surface-400 hover:text-white")}
          >
            <Shuffle className="w-4 h-4" />
          </button>
          
          <button onClick={previous} className="text-surface-400 hover:text-white transition-colors">
            <SkipBack className="w-5 h-5 fill-current" />
          </button>
          
          <button 
            onClick={togglePlay}
            className="w-10 h-10 flex items-center justify-center rounded-full bg-white text-black hover:scale-105 transition-transform shadow-lg shadow-white/10"
          >
            {isPlaying ? (
              <Pause className="w-5 h-5 fill-current" />
            ) : (
              <Play className="w-5 h-5 fill-current ml-1" />
            )}
          </button>
          
          <button onClick={next} className="text-surface-400 hover:text-white transition-colors">
            <SkipForward className="w-5 h-5 fill-current" />
          </button>
          
          <button 
            onClick={cycleRepeat}
            className={cn("transition-colors", repeatMode !== 'off' ? "text-primary-400" : "text-surface-400 hover:text-white")}
          >
            <Repeat className="w-4 h-4" />
          </button>
        </div>
        
        <div className="flex items-center gap-2 w-full max-w-md">
          <span className="text-[11px] text-surface-400 font-medium w-10 text-right">{formatTime(progress)}</span>
          
          <input
            type="range"
            min={0}
            max={duration || 100}
            value={progress}
            onChange={handleProgressChange}
            className="player-slider flex-1"
          />
          
          <span className="text-[11px] text-surface-400 font-medium w-10 text-left">{formatTime(duration)}</span>
        </div>
      </div>

      {/* Volume */}
      <div className="w-1/3 flex items-center justify-end gap-3">
        <button onClick={toggleMute} className="text-surface-400 hover:text-white transition-colors">
          {volume === 0 ? <VolumeX className="w-5 h-5" /> : <Volume2 className="w-5 h-5" />}
        </button>
        <input
          type="range"
          min={0}
          max={1}
          step={0.01}
          value={volume}
          onChange={handleVolumeChange}
          className="player-slider w-24"
        />
      </div>
    </div>
  )
}
