import { Play } from 'lucide-react'
import type { Playlist } from '@/types'
import { cn } from '@/utils/cn'

interface PlaylistCardProps {
  playlist: Playlist
  onClick?: (playlist: Playlist) => void
  className?: string
}

export function PlaylistCard({ playlist, onClick, className }: PlaylistCardProps) {
  return (
    <div
      className={cn(
        'group relative p-4 rounded-xl bg-surface-900/40 hover:bg-surface-800 transition-all duration-300 cursor-pointer overflow-hidden border border-transparent hover:border-white/5',
        className
      )}
      onClick={() => onClick?.(playlist)}
    >
      <div className="relative aspect-square mb-4 rounded-lg overflow-hidden shadow-lg">
        {playlist.cover_url ? (
          <img
            src={playlist.cover_url}
            alt={playlist.name}
            className="object-cover w-full h-full transform group-hover:scale-105 transition-transform duration-500"
            loading="lazy"
          />
        ) : (
          <div className="w-full h-full bg-surface-800 flex items-center justify-center">
            <span className="text-surface-400">No cover</span>
          </div>
        )}
        
        {/* Play Button Overlay */}
        <div className="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center backdrop-blur-[2px]">
          <button className="w-12 h-12 rounded-full bg-primary-500 text-white flex items-center justify-center shadow-xl shadow-primary-500/30 transform translate-y-4 group-hover:translate-y-0 transition-all duration-300 hover:scale-110 hover:bg-primary-400">
            <Play className="w-6 h-6 fill-current ml-1" />
          </button>
        </div>
      </div>

      <div className="flex flex-col">
        <h3 className="font-bold text-white truncate group-hover:text-primary-400 transition-colors">
          {playlist.name}
        </h3>
        <p className="text-sm text-surface-400 truncate mt-1">
          {playlist.track_count} {playlist.track_count === 1 ? 'song' : 'songs'}
        </p>
      </div>
    </div>
  )
}
