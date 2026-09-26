import { useParams, useNavigate } from 'react-router-dom'
import { useArtist } from '@/hooks/useMusic'
import { AlbumCard } from '@/components/cards/AlbumCard'
import { Play } from 'lucide-react'
import { usePlayerStore } from '@/store/playerStore'

export function ArtistPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const { data: artist, isLoading, isError } = useArtist(id!)
  const { setTrack, playQueue } = usePlayerStore()

  if (isLoading) {
    return (
      <div className="flex justify-center py-32">
        <div className="w-10 h-10 border-4 border-surface-800 border-t-primary-500 rounded-full animate-spin" />
      </div>
    )
  }

  if (isError || !artist) {
    return (
      <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-6 text-center mt-10">
        <p className="text-red-400">Failed to load artist. They might not exist.</p>
      </div>
    )
  }

  return (
    <div className="flex flex-col gap-8 animate-in fade-in duration-700">
      {/* Hero Section */}
      <div className="relative h-80 -mt-8 -mx-8 px-8 flex items-end pb-8 overflow-hidden">
        <div className="absolute inset-0 z-0">
          {artist.picture_url && (
            <img
              src={artist.picture_url}
              alt={artist.name}
              className="w-full h-full object-cover opacity-40 blur-sm"
            />
          )}
          <div className="absolute inset-0 bg-gradient-to-t from-surface-950 via-surface-950/60 to-transparent" />
        </div>
        
        <div className="relative z-10 flex items-center gap-8 w-full">
          {artist.picture_url ? (
            <img
              src={artist.picture_url}
              alt={artist.name}
              className="w-48 h-48 rounded-full shadow-2xl object-cover border-4 border-surface-950"
            />
          ) : (
            <div className="w-48 h-48 rounded-full bg-surface-800 flex items-center justify-center shadow-2xl border-4 border-surface-950">
              <span className="text-surface-400">No Photo</span>
            </div>
          )}
          
          <div className="flex flex-col">
            <span className="text-sm font-bold uppercase tracking-widest text-surface-400 mb-2">
              Artist
            </span>
            <h1 className="text-6xl font-extrabold text-white mb-6 tracking-tight">
              {artist.name}
            </h1>
            <p className="text-surface-300 font-medium">
              {new Intl.NumberFormat('en-US').format(artist.fan_count)} Fans
            </p>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-4 my-2">
        <button 
          onClick={() => playQueue(artist.top_tracks)}
          className="w-14 h-14 rounded-full bg-primary-500 text-white flex items-center justify-center shadow-xl shadow-primary-500/30 hover:scale-105 hover:bg-primary-400 transition-all"
        >
          <Play className="w-7 h-7 fill-current ml-1" />
        </button>
      </div>

      {/* Top Tracks */}
      {artist.top_tracks && artist.top_tracks.length > 0 && (
        <section>
          <h2 className="text-2xl font-bold text-white mb-6">Popular</h2>
          <div className="flex flex-col gap-2">
            {artist.top_tracks.slice(0, 5).map((track, i) => (
              <div
                key={track.id}
                onClick={() => setTrack(track, artist.top_tracks)}
                className="flex items-center gap-4 p-3 rounded-lg hover:bg-white/5 transition-colors group cursor-pointer"
              >
                <div className="w-8 text-center text-surface-400 group-hover:hidden">
                  {i + 1}
                </div>
                <div className="w-8 flex justify-center hidden group-hover:flex text-white">
                  <Play className="w-4 h-4 fill-current" />
                </div>
                <img
                  src={track.cover_url || ''}
                  alt={track.title}
                  className="w-10 h-10 rounded object-cover"
                />
                <div className="flex-1">
                  <h4 className="text-white font-medium group-hover:text-primary-400 transition-colors">
                    {track.title}
                  </h4>
                </div>
                <div className="text-surface-400 text-sm">
                  {Math.floor(track.duration_ms / 60000)}:
                  {String(Math.floor((track.duration_ms % 60000) / 1000)).padStart(2, '0')}
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Albums */}
      {artist.albums && artist.albums.length > 0 && (
        <section className="mt-8">
          <h2 className="text-2xl font-bold text-white mb-6">Discography</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
            {artist.albums.map((album) => (
              <AlbumCard key={album.id} album={album} onClick={() => navigate(`/album/${album.id}`)} />
            ))}
          </div>
        </section>
      )}
    </div>
  )
}
