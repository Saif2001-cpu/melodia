import { Outlet } from 'react-router-dom'
import { Sidebar } from '@/components/sidebar/Sidebar'
import { Player } from '@/components/player/Player'

/**
 * Main application layout with sidebar, content area, and persistent player.
 */
export function MainLayout() {
  return (
    <div className="flex flex-col h-screen bg-surface-950 text-white overflow-hidden selection:bg-primary-500/30 selection:text-white">
      {/* Top Section: Sidebar + Main Content */}
      <div className="flex flex-1 overflow-hidden">
        <Sidebar />

        <main className="flex-1 overflow-y-auto bg-gradient-to-b from-surface-900 to-surface-950 relative">
          {/* Main content container with some padding */}
          <div className="p-8 pb-32 min-h-full">
            <Outlet />
          </div>
        </main>
      </div>

      {/* Bottom Section: Persistent Player */}
      <div className="absolute bottom-0 w-full z-50">
        <Player />
      </div>
    </div>
  )
}
