import { useParams } from 'react-router-dom'
import { useAlbum } from '@/hooks/useMusic'
import { Play, Clock } from 'lucide-react'
import { usePlayerStore } from '@/store/playerStore'

export function AlbumPage() {
  const { id } = useParams<{ id: string }>()
  const { data: album, isLoading, isError } = useAlbum(id!)
  const { setTrack, playQueue } = usePlayerStore()

  if (isLoading) {
    return (
      <div className="flex justify-center py-32">
        <div className="w-10 h-10 border-4 border-surface-800 border-t-primary-500 rounded-full animate-spin" />
      </div>
    )
  }

  if (isError || !album) {
    return (
      <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-6 text-center mt-10">
        <p className="text-red-400">Failed to load album. It might not exist.</p>
      </div>
    )
  }

  const totalDuration = album.tracks.reduce((acc, t) => acc + t.duration_ms, 0)
  const totalMins = Math.floor(totalDuration / 60000)

  return (
    <div className="flex flex-col gap-8 animate-in fade-in duration-700">
      {/* Hero Section */}
      <div className="flex items-end gap-8 mt-4 mb-8">
        {album.cover_url ? (
          <img
            src={album.cover_url}
            alt={album.title}
            className="w-56 h-56 rounded-xl shadow-2xl object-cover"
          />
        ) : (
          <div className="w-56 h-56 rounded-xl bg-surface-800 flex items-center justify-center shadow-2xl">
            <span className="text-surface-400">No Cover</span>
          </div>
        )}
        
        <div className="flex flex-col">
          <span className="text-sm font-bold uppercase tracking-widest text-surface-400 mb-2">
            Album
          </span>
          <h1 className="text-5xl font-extrabold text-white mb-6 tracking-tight">
            {album.title}
          </h1>
          <div className="flex items-center gap-2 text-sm text-surface-300 font-medium">
            <span className="text-white hover:underline cursor-pointer">{album.artist_name}</span>
            <span>•</span>
            <span>{album.release_date?.substring(0, 4) || 'Unknown Year'}</span>
            <span>•</span>
            <span>{album.track_count} songs, {totalMins} min</span>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-4 my-2">
        <button 
          onClick={() => playQueue(album.tracks)}
          className="w-14 h-14 rounded-full bg-primary-500 text-white flex items-center justify-center shadow-xl shadow-primary-500/30 hover:scale-105 hover:bg-primary-400 transition-all"
        >
          <Play className="w-7 h-7 fill-current ml-1" />
        </button>
      </div>

      {/* Tracks Table */}
      {album.tracks && album.tracks.length > 0 && (
        <div className="mt-4">
          <div className="flex items-center text-surface-400 text-sm font-medium border-b border-white/5 pb-2 mb-4 px-4">
            <div className="w-12">#</div>
            <div className="flex-1">Title</div>
            <div className="w-16 flex justify-end">
              <Clock className="w-4 h-4" />
            </div>
          </div>

          <div className="flex flex-col gap-1">
            {album.tracks.map((track, i) => (
              <div
                key={track.id}
                onClick={() => setTrack(track, album.tracks)}
                className="flex items-center px-4 py-3 rounded-lg hover:bg-white/5 transition-colors group cursor-pointer"
              >
                <div className="w-12 text-surface-400 group-hover:hidden">
                  {i + 1}
                </div>
                <div className="w-12 hidden group-hover:flex text-white">
                  <Play className="w-4 h-4 fill-current" />
                </div>
                <div className="flex-1 flex flex-col">
                  <span className="text-white font-medium group-hover:text-primary-400 transition-colors">
                    {track.title}
                  </span>
                  <span className="text-sm text-surface-400">
                    {track.artist_name}
                  </span>
                </div>
                <div className="w-16 text-right text-surface-400 text-sm">
                  {Math.floor(track.duration_ms / 60000)}:
                  {String(Math.floor((track.duration_ms % 60000) / 1000)).padStart(2, '0')}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
