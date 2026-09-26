import { useTrending, useRecommendations } from '@/hooks/useMusic'
import { usePlayHistory } from '@/hooks/useLibrary'
import { TrackCard } from '@/components/cards/TrackCard'
import { useAuthStore } from '@/store/authStore'
import { usePlayerStore } from '@/store/playerStore'
import { format } from 'date-fns'

export function HomePage() {
  const { user } = useAuthStore()
  const { data: trendingTracks, isLoading: trendingLoading } = useTrending(10)
  const { data: recommendedTracks, isLoading: recLoading } = useRecommendations(10)
  const { data: historyPage } = usePlayHistory(1, 10)
  const setTrack = usePlayerStore((s) => s.setTrack)

  const recentTracks = historyPage?.items || []

  // Determine greeting based on time of day
  const hour = parseInt(format(new Date(), 'H'), 10)
  let greeting = 'Good evening'
  if (hour < 12) greeting = 'Good morning'
  else if (hour < 17) greeting = 'Good afternoon'

  return (
    <div className="flex flex-col gap-8 animate-in fade-in duration-700">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-extrabold tracking-tight text-white mb-2">
            {greeting}
          </h1>
          {user && (
            <p className="text-surface-400">
              Welcome back, <span className="text-primary-400">{user.username}</span>
            </p>
          )}
        </div>
      </header>

      {/* Recommendations Section */}
      <section>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-white">Made For You</h2>
        </div>

        {recLoading ? (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="bg-surface-900/50 rounded-xl p-4 animate-pulse">
                <div className="aspect-square bg-surface-800 rounded-lg mb-4" />
                <div className="h-4 bg-surface-800 rounded w-3/4 mb-2" />
                <div className="h-3 bg-surface-800 rounded w-1/2" />
              </div>
            ))}
          </div>
        ) : recommendedTracks && recommendedTracks.length > 0 ? (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
            {recommendedTracks.map((track) => (
              <TrackCard
                key={track.id}
                track={track}
                onClick={(t) => setTrack(t, recommendedTracks)}
              />
            ))}
          </div>
        ) : null}
      </section>

      {/* Recently Played Section */}
      {recentTracks.length > 0 && (
        <section>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-white">Recently Played</h2>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
            {recentTracks.slice(0, 5).map((track) => (
              <TrackCard
                key={track.id}
                track={track}
                onClick={(t) => setTrack(t, recentTracks)}
              />
            ))}
          </div>
        </section>
      )}

      {/* Trending Section */}
      <section>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-white">Trending Now</h2>
        </div>

        {trendingLoading ? (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
            {Array.from({ length: 5 }).map((_, i) => (
              <div key={i} className="bg-surface-900/50 rounded-xl p-4 animate-pulse">
                <div className="aspect-square bg-surface-800 rounded-lg mb-4" />
                <div className="h-4 bg-surface-800 rounded w-3/4 mb-2" />
                <div className="h-3 bg-surface-800 rounded w-1/2" />
              </div>
            ))}
          </div>
        ) : trendingTracks && trendingTracks.length > 0 ? (
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
            {trendingTracks.map((track) => (
              <TrackCard
                key={track.id}
                track={track}
                onClick={(t) => setTrack(t, trendingTracks)}
              />
            ))}
          </div>
        ) : (
          <div className="bg-red-500/10 border border-red-500/20 rounded-xl p-6 text-center">
            <p className="text-red-400">Failed to load trending tracks. Please try again later.</p>
          </div>
        )}
      </section>
    </div>
  )
}
