import type { Artist } from '@/types'
import { cn } from '@/utils/cn'

interface ArtistCardProps {
  artist: Artist
  onClick?: (artist: Artist) => void
  className?: string
}

export function ArtistCard({ artist, onClick, className }: ArtistCardProps) {
  return (
    <div
      className={cn(
        'group p-4 rounded-xl bg-surface-900/40 hover:bg-surface-800 transition-all duration-300 cursor-pointer border border-transparent hover:border-white/5 flex flex-col items-center text-center',
        className
      )}
      onClick={() => onClick?.(artist)}
    >
      <div className="relative aspect-square w-full mb-4 rounded-full overflow-hidden shadow-lg shadow-surface-900/50">
        {artist.picture_url ? (
          <img
            src={artist.picture_url}
            alt={artist.name}
            className="object-cover w-full h-full transform group-hover:scale-105 transition-transform duration-500"
            loading="lazy"
          />
        ) : (
          <div className="w-full h-full bg-surface-800 flex items-center justify-center">
            <span className="text-surface-400">No photo</span>
          </div>
        )}
      </div>

      <h3 className="font-bold text-white truncate w-full group-hover:text-secondary-400 transition-colors">
        {artist.name}
      </h3>
      <p className="text-sm text-surface-400 truncate mt-1">Artist</p>
    </div>
  )
}
