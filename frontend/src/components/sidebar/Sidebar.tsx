import { NavLink, useNavigate } from 'react-router-dom'
import { Home, Search, Library, PlusCircle, Heart, LogOut } from 'lucide-react'
import { useAuthStore } from '@/store/authStore'
import { usePlaylists, useCreatePlaylist } from '@/hooks/usePlaylists'
import { cn } from '@/utils/cn'

export function Sidebar() {
  const { logout } = useAuthStore()
  const navigate = useNavigate()
  
  const { data: playlists } = usePlaylists(1, 50)
  const createPlaylist = useCreatePlaylist()

  const navItems = [
    { label: 'Home', icon: Home, to: '/' },
    { label: 'Search', icon: Search, to: '/search' },
    { label: 'Your Library', icon: Library, to: '/library' },
  ]

  const handleCreatePlaylist = () => {
    createPlaylist.mutate(
      {
        name: `New Playlist #${(playlists?.items?.length || 0) + 1}`,
        description: 'My awesome new playlist',
      },
      {
        onSuccess: (newPlaylist) => {
          navigate(`/playlist/${newPlaylist.id}`)
        },
      }
    )
  }

  return (
    <aside className="w-64 h-full flex flex-col bg-surface-950/80 backdrop-blur-xl border-r border-white/5 p-6 gap-8 relative z-20">
      {/* Brand */}
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-primary-500 to-secondary-500 flex items-center justify-center shadow-lg shadow-primary-500/20">
          <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
          </svg>
        </div>
        <span className="text-2xl font-bold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-primary-400 to-secondary-400 cursor-pointer" onClick={() => navigate('/')}>
          Melodia
        </span>
      </div>

      {/* Main Nav */}
      <nav className="flex flex-col gap-2">
        {navItems.map((item) => (
          <NavLink
            key={item.label}
            to={item.to}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-4 px-4 py-3 rounded-xl font-medium transition-all duration-300',
                isActive
                  ? 'bg-white/10 text-white shadow-sm'
                  : 'text-surface-400 hover:text-white hover:bg-white/5'
              )
            }
          >
            <item.icon className="w-5 h-5" />
            {item.label}
          </NavLink>
        ))}
      </nav>

      {/* User Actions */}
      <div className="flex flex-col gap-2 mt-2">
        <button 
          onClick={handleCreatePlaylist}
          disabled={createPlaylist.isPending}
          className="flex items-center gap-4 px-4 py-3 rounded-xl font-medium text-surface-400 hover:text-white hover:bg-white/5 transition-all duration-300 group disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <div className="w-5 h-5 bg-surface-800 rounded-sm flex items-center justify-center group-hover:bg-white/20 transition-colors">
            {createPlaylist.isPending ? (
              <div className="w-3 h-3 border-2 border-surface-400 border-t-white rounded-full animate-spin" />
            ) : (
              <PlusCircle className="w-4 h-4" />
            )}
          </div>
          Create Playlist
        </button>
        <NavLink
          to="/liked"
          className={({ isActive }) =>
            cn(
              'flex items-center gap-4 px-4 py-3 rounded-xl font-medium transition-all duration-300 group',
              isActive
                ? 'bg-white/10 text-white shadow-sm'
                : 'text-surface-400 hover:text-white hover:bg-white/5'
            )
          }
        >
          <div className="w-5 h-5 bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 rounded-sm flex items-center justify-center shadow-md">
            <Heart className="w-3 h-3 text-white" fill="currentColor" />
          </div>
          Liked Songs
        </NavLink>
      </div>

      <div className="h-[1px] bg-white/5 w-full my-2"></div>

      {/* Playlists List */}
      <div className="flex-1 overflow-y-auto scrollbar-thin scrollbar-thumb-surface-700 scrollbar-track-transparent pr-2 flex flex-col gap-1">
        {playlists?.items?.map((playlist) => (
          <NavLink
            key={playlist.id}
            to={`/playlist/${playlist.id}`}
            className={({ isActive }) =>
              cn(
                'px-4 py-2 rounded-lg text-sm font-medium transition-colors truncate',
                isActive ? 'text-white bg-white/5' : 'text-surface-400 hover:text-white'
              )
            }
          >
            {playlist.name}
          </NavLink>
        ))}
      </div>

      <div className="mt-auto pt-4 border-t border-white/5">
        <button
          onClick={logout}
          className="w-full flex items-center gap-4 px-4 py-3 rounded-xl font-medium text-surface-400 hover:text-red-400 hover:bg-red-500/10 transition-all duration-300"
        >
          <LogOut className="w-5 h-5" />
          Log Out
        </button>
      </div>
    </aside>
  )
}
