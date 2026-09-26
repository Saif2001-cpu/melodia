import { Outlet } from 'react-router-dom'

/**
 * Minimal centered layout for login/register pages.
 */
export function AuthLayout() {
  return (
    <div className="min-h-screen bg-surface-950 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold gradient-text">Melodia</h1>
          <p className="text-surface-400 mt-2">Your music, your world.</p>
        </div>
        <div className="glass rounded-2xl p-8">
          <Outlet />
        </div>
      </div>
    </div>
  )
}
