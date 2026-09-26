import { useParams } from 'react-router-dom'
import { usePlaylist, useRemoveTrackFromPlaylist } from '@/hooks/usePlaylists'
import { usePlayerStore } from '@/store/playerStore'
import { Play, Clock, Trash2, ListMusic } from 'lucide-react'
import { usePlaylistWebSocket } from '@/hooks/usePlaylistWebSocket'

export function PlaylistPage() {
  const { id } = useParams<{ id: string }>()
  const { data: playlist, isLoading, isError } = usePlaylist(id!)
  const { setTrack, playQueue } = usePlayerStore()
  const removeTrack = useRemoveTrackFromPlaylist()

  usePlaylistWebSocket(id)

  if (isLoading) {
    return (
      <div className="flex justify-center py-32">
        <div className="w-10 h-10 border-4 border-surface-800 border-t-primary-500 rounded-full animate-spin" />
      </div>
    )
  }

  if (isError || !playlist) {
    return (
      <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-6 text-center mt-10">
        <p className="text-red-400">Failed to load playlist. It might not exist.</p>
      </div>
    )
  }

  const tracks = playlist.tracks.map(pt => pt.track)
  const totalDuration = tracks.reduce((acc, t) => acc + t.duration_ms, 0)
  const totalMins = Math.floor(totalDuration / 60000)

  return (
    <div className="flex flex-col gap-8 animate-in fade-in duration-700">
      {/* Hero Section */}
      <div className="flex items-end gap-8 mt-4 mb-8">
        {playlist.cover_url ? (
          <img
            src={playlist.cover_url}
            alt={playlist.name}
            className="w-56 h-56 rounded-xl shadow-2xl object-cover"
          />
        ) : (
          <div className="w-56 h-56 rounded-xl bg-surface-800 flex items-center justify-center shadow-2xl border border-white/5">
            <ListMusic className="w-16 h-16 text-surface-400" />
          </div>
        )}
        
        <div className="flex flex-col">
          <span className="text-sm font-bold uppercase tracking-widest text-surface-400 mb-2">
            Playlist
          </span>
          <h1 className="text-5xl font-extrabold text-white mb-6 tracking-tight">
            {playlist.name}
          </h1>
          <div className="flex items-center gap-2 text-sm text-surface-300 font-medium">
            <span className="text-white">{playlist.owner_name || 'You'}</span>
            <span>•</span>
            <span>{playlist.track_count} songs, {totalMins} min</span>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-4 my-2">
        <button 
          onClick={() => playQueue(tracks)}
          className="w-14 h-14 rounded-full bg-primary-500 text-white flex items-center justify-center shadow-xl shadow-primary-500/30 hover:scale-105 hover:bg-primary-400 transition-all"
        >
          <Play className="w-7 h-7 fill-current ml-1" />
        </button>
      </div>

      {/* Tracks Table */}
      {tracks && tracks.length > 0 ? (
        <div className="mt-4">
          <div className="flex items-center text-surface-400 text-sm font-medium border-b border-white/5 pb-2 mb-4 px-4">
            <div className="w-12">#</div>
            <div className="flex-1">Title</div>
            <div className="w-16 flex justify-end">
              <Clock className="w-4 h-4" />
            </div>
            <div className="w-10"></div>
          </div>

          <div className="flex flex-col gap-1">
            {tracks.map((track, i) => (
              <div
                key={track.id}
                className="flex items-center px-4 py-3 rounded-lg hover:bg-white/5 transition-colors group cursor-pointer"
              >
                <div 
                  className="w-12 text-surface-400 group-hover:hidden"
                  onClick={() => setTrack(track, tracks)}
                >
                  {i + 1}
                </div>
                <div 
                  className="w-12 hidden group-hover:flex text-white"
                  onClick={() => setTrack(track, tracks)}
                >
                  <Play className="w-4 h-4 fill-current" />
                </div>
                
                <div className="flex-1 flex items-center gap-3" onClick={() => setTrack(track, tracks)}>
                  <img src={track.cover_url || ''} className="w-10 h-10 rounded object-cover" alt="" />
                  <div className="flex flex-col">
                    <span className="text-white font-medium group-hover:text-primary-400 transition-colors">
                      {track.title}
                    </span>
                    <span className="text-sm text-surface-400">
                      {track.artist_name}
                    </span>
                  </div>
                </div>
                
                <div className="w-16 text-right text-surface-400 text-sm" onClick={() => setTrack(track, tracks)}>
                  {Math.floor(track.duration_ms / 60000)}:
                  {String(Math.floor((track.duration_ms % 60000) / 1000)).padStart(2, '0')}
                </div>
                
                <div className="w-10 flex justify-end opacity-0 group-hover:opacity-100 transition-opacity">
                  <button 
                    onClick={(e) => {
                      e.stopPropagation()
                      removeTrack.mutate({ playlistId: playlist.id, trackId: track.id })
                    }}
                    className="text-surface-400 hover:text-red-400 p-1 rounded hover:bg-white/10 transition-colors"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="text-center py-20 bg-surface-900/50 rounded-xl border border-white/5 mt-4">
          <h3 className="text-xl font-bold text-white mb-2">No Songs Yet</h3>
          <p className="text-surface-400">Search for songs and add them to this playlist.</p>
        </div>
      )}
    </div>
  )
}
