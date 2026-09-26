import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Search as SearchIcon } from 'lucide-react'
import { useSearch } from '@/hooks/useMusic'
import { TrackCard } from '@/components/cards/TrackCard'
import { AlbumCard } from '@/components/cards/AlbumCard'
import { ArtistCard } from '@/components/cards/ArtistCard'
import { useDebounce } from '@/hooks/useDebounce'
import { usePlayerStore } from '@/store/playerStore'

export function SearchPage() {
  const navigate = useNavigate()
  const [query, setQuery] = useState('')
  const debouncedQuery = useDebounce(query, 500)
  const { data, isLoading, isError } = useSearch(debouncedQuery)
  const setTrack = usePlayerStore((s) => s.setTrack)

  return (
    <div className="flex flex-col gap-8 animate-in fade-in duration-500">
      {/* Search Header */}
      <div className="sticky top-0 z-10 bg-surface-950/80 backdrop-blur-xl py-4 -mx-8 px-8 border-b border-white/5">
        <div className="relative max-w-md">
          <SearchIcon className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-surface-400" />
          <input
            type="text"
            placeholder="What do you want to listen to?"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full bg-surface-900 border border-white/10 rounded-full py-3 pl-12 pr-4 text-white placeholder-surface-400 focus:outline-none focus:border-primary-500 focus:ring-1 focus:ring-primary-500 transition-all shadow-inner"
          />
        </div>
      </div>

      {!debouncedQuery && (
        <div className="flex flex-col items-center justify-center py-32 text-center">
          <SearchIcon className="w-16 h-16 text-surface-800 mb-6" />
          <h2 className="text-2xl font-bold text-white mb-2">Search Melodia</h2>
          <p className="text-surface-400">Find your favorite songs, artists, and albums.</p>
        </div>
      )}

      {isLoading && (
        <div className="flex justify-center py-20">
          <div className="w-10 h-10 border-4 border-surface-800 border-t-primary-500 rounded-full animate-spin" />
        </div>
      )}

      {isError && (
        <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-6 text-center">
          <p className="text-red-400">Failed to load search results. Please try again.</p>
        </div>
      )}

      {data && (
        <div className="flex flex-col gap-10">
          {/* Top Result / Tracks */}
          {data.tracks.length > 0 && (
            <section>
              <h2 className="text-2xl font-bold text-white mb-6">Songs</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
                {data.tracks.slice(0, 5).map((track) => (
                  <TrackCard key={track.id} track={track} onClick={(t) => setTrack(t, data.tracks)} />
                ))}
              </div>
            </section>
          )}

          {/* Artists */}
          {data.artists.length > 0 && (
            <section>
              <h2 className="text-2xl font-bold text-white mb-6">Artists</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
                {data.artists.slice(0, 5).map((artist) => (
                  <ArtistCard key={artist.id} artist={artist} onClick={() => navigate(`/artist/${artist.id}`)} />
                ))}
              </div>
            </section>
          )}

          {/* Albums */}
          {data.albums.length > 0 && (
            <section>
              <h2 className="text-2xl font-bold text-white mb-6">Albums</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
                {data.albums.slice(0, 5).map((album) => (
                  <AlbumCard key={album.id} album={album} onClick={() => navigate(`/album/${album.id}`)} />
                ))}
              </div>
            </section>
          )}

          {data.tracks.length === 0 && data.artists.length === 0 && data.albums.length === 0 && (
            <div className="text-center py-20">
              <p className="text-lg text-surface-400">No results found for "{debouncedQuery}"</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
