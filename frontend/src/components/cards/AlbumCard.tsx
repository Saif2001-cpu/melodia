import type { Album } from '@/types'
import { cn } from '@/utils/cn'

interface AlbumCardProps {
  album: Album
  onClick?: (album: Album) => void
  className?: string
}

export function AlbumCard({ album, onClick, className }: AlbumCardProps) {
  return (
    <div
      className={cn(
        'group p-4 rounded-xl bg-surface-900/40 hover:bg-surface-800 transition-all duration-300 cursor-pointer border border-transparent hover:border-white/5',
        className
      )}
      onClick={() => onClick?.(album)}
    >
      <div className="relative aspect-square mb-4 rounded-lg overflow-hidden shadow-lg">
        {album.cover_url ? (
          <img
            src={album.cover_url}
            alt={album.title}
            className="object-cover w-full h-full transform group-hover:scale-105 transition-transform duration-500"
            loading="lazy"
          />
        ) : (
          <div className="w-full h-full bg-surface-800 flex items-center justify-center">
            <span className="text-surface-400">No cover</span>
          </div>
        )}
      </div>

      <div className="flex flex-col">
        <h3 className="font-bold text-white truncate group-hover:text-primary-400 transition-colors">
          {album.title}
        </h3>
        <p className="text-sm text-surface-400 truncate mt-1">
          {album.artist_name} • Album
        </p>
      </div>
    </div>
  )
}
