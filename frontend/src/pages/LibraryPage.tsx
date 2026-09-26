import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { usePlaylists, useCreatePlaylist } from '@/hooks/usePlaylists'
import { useSavedAlbums } from '@/hooks/useLibrary'
import { PlaylistCard } from '@/components/cards/PlaylistCard'
import { AlbumCard } from '@/components/cards/AlbumCard'
import { ListMusic, Disc3, Plus } from 'lucide-react'
import { cn } from '@/utils/cn'

type Tab = 'playlists' | 'albums'

export function LibraryPage() {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState<Tab>('playlists')
  
  const { data: playlists, isLoading: loadingPlaylists } = usePlaylists(1, 50)
  const { data: albums, isLoading: loadingAlbums } = useSavedAlbums(1, 50)
  const createPlaylist = useCreatePlaylist()

  const handleCreatePlaylist = () => {
    createPlaylist.mutate(
      { name: `New Playlist #${(playlists?.items?.length || 0) + 1}` },
      { onSuccess: (p) => navigate(`/playlist/${p.id}`) }
    )
  }

  return (
    <div className="flex flex-col gap-8 animate-in fade-in duration-500">
      <header className="flex flex-col gap-6">
        <div className="flex items-center justify-between">
          <h1 className="text-4xl font-extrabold tracking-tight text-white">Your Library</h1>
          <button
            onClick={handleCreatePlaylist}
            disabled={createPlaylist.isPending}
            className="flex items-center gap-2 bg-primary-500 hover:bg-primary-400 text-white px-4 py-2 rounded-full font-medium transition-colors shadow-lg shadow-primary-500/20 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Plus className="w-5 h-5" />
            {createPlaylist.isPending ? 'Creating…' : 'Create Playlist'}
          </button>
        </div>

        {/* Tabs */}
        <div className="flex items-center gap-4 border-b border-white/5 pb-2">
          <button
            onClick={() => setActiveTab('playlists')}
            className={cn(
              "flex items-center gap-2 pb-2 border-b-2 transition-all font-medium",
              activeTab === 'playlists' 
                ? "border-primary-500 text-white" 
                : "border-transparent text-surface-400 hover:text-white"
            )}
          >
            <ListMusic className="w-5 h-5" />
            Playlists
          </button>
          <button
            onClick={() => setActiveTab('albums')}
            className={cn(
              "flex items-center gap-2 pb-2 border-b-2 transition-all font-medium",
              activeTab === 'albums' 
                ? "border-primary-500 text-white" 
                : "border-transparent text-surface-400 hover:text-white"
            )}
          >
            <Disc3 className="w-5 h-5" />
            Albums
          </button>
        </div>
      </header>

      {/* Playlists Content */}
      {activeTab === 'playlists' && (
        <section>
          {loadingPlaylists ? (
            <div className="flex justify-center py-20">
              <div className="w-10 h-10 border-4 border-surface-800 border-t-primary-500 rounded-full animate-spin" />
            </div>
          ) : playlists?.items.length ? (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
              {playlists.items.map((playlist) => (
                <PlaylistCard 
                  key={playlist.id} 
                  playlist={playlist} 
                  onClick={() => navigate(`/playlist/${playlist.id}`)}
                />
              ))}
            </div>
          ) : (
            <div className="text-center py-20 bg-surface-900/50 rounded-xl border border-white/5">
              <ListMusic className="w-12 h-12 text-surface-400 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-white mb-2">No Playlists Yet</h3>
              <p className="text-surface-400">Create your first playlist to start organizing your music.</p>
            </div>
          )}
        </section>
      )}

      {/* Albums Content */}
      {activeTab === 'albums' && (
        <section>
          {loadingAlbums ? (
            <div className="flex justify-center py-20">
              <div className="w-10 h-10 border-4 border-surface-800 border-t-primary-500 rounded-full animate-spin" />
            </div>
          ) : albums?.items.length ? (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
              {albums.items.map((album) => (
                <AlbumCard 
                  key={album.id} 
                  album={album} 
                  onClick={() => navigate(`/album/${album.id}`)}
                />
              ))}
            </div>
          ) : (
            <div className="text-center py-20 bg-surface-900/50 rounded-xl border border-white/5">
              <Disc3 className="w-12 h-12 text-surface-400 mx-auto mb-4" />
              <h3 className="text-xl font-bold text-white mb-2">No Saved Albums</h3>
              <p className="text-surface-400">Albums you save will appear here.</p>
            </div>
          )}
        </section>
      )}
    </div>
  )
}
