import { Play, SkipBack, SkipForward, Volume2, Repeat, Shuffle } from 'lucide-react'

export function PlayerPlaceholder() {
  return (
    <div className="h-24 w-full bg-surface-950/90 backdrop-blur-2xl border-t border-white/5 px-6 flex items-center justify-between relative z-30">
      {/* Track Info Placeholder */}
      <div className="w-1/3 flex items-center gap-4">
        <div className="w-14 h-14 rounded-lg bg-surface-800 animate-pulse shadow-md" />
        <div className="flex flex-col gap-2">
          <div className="w-32 h-4 bg-surface-800 rounded animate-pulse" />
          <div className="w-24 h-3 bg-surface-800/50 rounded animate-pulse" />
        </div>
      </div>

      {/* Controls Placeholder */}
      <div className="w-1/3 flex flex-col items-center gap-2">
        <div className="flex items-center gap-6">
          <button className="text-surface-400 hover:text-white transition-colors">
            <Shuffle className="w-5 h-5" />
          </button>
          <button className="text-surface-400 hover:text-white transition-colors">
            <SkipBack className="w-6 h-6 fill-current" />
          </button>
          <button className="w-10 h-10 flex items-center justify-center rounded-full bg-white text-black hover:scale-105 transition-transform shadow-lg shadow-white/10">
            <Play className="w-5 h-5 fill-current ml-1" />
          </button>
          <button className="text-surface-400 hover:text-white transition-colors">
            <SkipForward className="w-6 h-6 fill-current" />
          </button>
          <button className="text-surface-400 hover:text-white transition-colors">
            <Repeat className="w-5 h-5" />
          </button>
        </div>
        <div className="flex items-center gap-2 w-full max-w-md">
          <span className="text-xs text-surface-400 font-medium">0:00</span>
          <div className="flex-1 h-1.5 bg-surface-800 rounded-full overflow-hidden group cursor-pointer relative">
            <div className="w-0 h-full bg-primary-500 group-hover:bg-primary-400 transition-colors" />
          </div>
          <span className="text-xs text-surface-400 font-medium">0:00</span>
        </div>
      </div>

      {/* Volume Placeholder */}
      <div className="w-1/3 flex items-center justify-end gap-4">
        <Volume2 className="w-5 h-5 text-surface-400" />
        <div className="w-24 h-1.5 bg-surface-800 rounded-full overflow-hidden group cursor-pointer">
          <div className="w-2/3 h-full bg-white group-hover:bg-primary-400 transition-colors" />
        </div>
      </div>
    </div>
  )
}
