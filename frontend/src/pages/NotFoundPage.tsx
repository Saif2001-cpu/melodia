import { Link } from 'react-router-dom'
export function NotFoundPage() {
  return (
    <div className="min-h-screen bg-surface-950 flex flex-col items-center justify-center text-white">
      <h1 className="text-6xl font-bold gradient-text mb-4">404</h1>
      <p className="text-surface-400 mb-8">This page got lost in the shuffle.</p>
      <Link to="/" className="px-6 py-3 bg-brand-500 rounded-full hover:bg-brand-400 transition-colors">Go Home</Link>
    </div>
  )
}
