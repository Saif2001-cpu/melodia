import { useLikedSongs, useUnlikeTrack } from '@/hooks/useLibrary'
import { usePlayerStore } from '@/store/playerStore'
import { Play, Clock, Heart } from 'lucide-react'

export function LikedSongsPage() {
  const { data: pageData, isLoading, isError } = useLikedSongs(1, 100)
  const { setTrack, playQueue } = usePlayerStore()
  const unlikeTrack = useUnlikeTrack()

  if (isLoading) {
    return (
      <div className="flex justify-center py-32">
        <div className="w-10 h-10 border-4 border-surface-800 border-t-primary-500 rounded-full animate-spin" />
      </div>
    )
  }

  if (isError) {
    return (
      <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-6 text-center mt-10">
        <p className="text-red-400">Failed to load liked songs.</p>
      </div>
    )
  }

  const tracks = pageData?.items || []
  const totalDuration = tracks.reduce((acc, t) => acc + t.duration_ms, 0)
  const totalMins = Math.floor(totalDuration / 60000)

  return (
    <div className="flex flex-col gap-8 animate-in fade-in duration-700">
      {/* Hero Section */}
      <div className="flex items-end gap-8 mt-4 mb-8">
        <div className="w-56 h-56 rounded-xl bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center shadow-2xl">
          <Heart className="w-24 h-24 text-white fill-current shadow-black" />
        </div>
        
        <div className="flex flex-col">
          <span className="text-sm font-bold uppercase tracking-widest text-surface-400 mb-2">
            Playlist
          </span>
          <h1 className="text-5xl font-extrabold text-white mb-6 tracking-tight">
            Liked Songs
          </h1>
          <div className="flex items-center gap-2 text-sm text-surface-300 font-medium">
            <span className="text-white">You</span>
            <span>•</span>
            <span>{tracks.length} songs, {totalMins} min</span>
          </div>
        </div>
      </div>

      <div className="flex items-center gap-4 my-2">
        <button 
          onClick={() => playQueue(tracks)}
          disabled={tracks.length === 0}
          className="w-14 h-14 rounded-full bg-primary-500 text-white flex items-center justify-center shadow-xl shadow-primary-500/30 hover:scale-105 hover:bg-primary-400 transition-all disabled:opacity-50 disabled:hover:scale-100"
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
            <div className="flex-1 hidden md:block">Album</div>
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
                    <span className="text-sm text-surface-400 hover:underline">
                      {track.artist_name}
                    </span>
                  </div>
                </div>

                <div className="flex-1 hidden md:flex items-center text-sm text-surface-400 hover:text-white transition-colors" onClick={() => setTrack(track, tracks)}>
                  {track.album_title}
                </div>
                
                <div className="w-16 text-right text-surface-400 text-sm" onClick={() => setTrack(track, tracks)}>
                  {Math.floor(track.duration_ms / 60000)}:
                  {String(Math.floor((track.duration_ms % 60000) / 1000)).padStart(2, '0')}
                </div>
                
                <div className="w-10 flex justify-end opacity-0 group-hover:opacity-100 transition-opacity">
                  <button 
                    onClick={(e) => {
                      e.stopPropagation()
                      unlikeTrack.mutate(track.id)
                    }}
                    className="text-primary-500 hover:text-white p-1 rounded hover:bg-white/10 transition-colors"
                  >
                    <Heart className="w-5 h-5 fill-current" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="text-center py-20 bg-surface-900/50 rounded-xl border border-white/5 mt-4">
          <Heart className="w-12 h-12 text-surface-400 mx-auto mb-4" />
          <h3 className="text-xl font-bold text-white mb-2">Songs you like will appear here</h3>
          <p className="text-surface-400">Save songs by tapping the heart icon.</p>
        </div>
      )}
    </div>
  )
}
