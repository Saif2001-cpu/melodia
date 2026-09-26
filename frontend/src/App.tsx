import { Routes, Route, Navigate } from 'react-router-dom'
import { MainLayout } from '@/layouts/MainLayout'
import { AuthLayout } from '@/layouts/AuthLayout'
import { HomePage } from '@/pages/HomePage'
import { SearchPage } from '@/pages/SearchPage'
import { LibraryPage } from '@/pages/LibraryPage'
import { PlaylistPage } from '@/pages/PlaylistPage'
import { ArtistPage } from '@/pages/ArtistPage'
import { AlbumPage } from '@/pages/AlbumPage'
import { LikedSongsPage } from '@/pages/LikedSongsPage'
import { LoginPage } from '@/pages/LoginPage'
import { RegisterPage } from '@/pages/RegisterPage'
import { ProfilePage } from '@/pages/ProfilePage'
import { NotFoundPage } from '@/pages/NotFoundPage'
import { useAuthStore } from '@/store/authStore'

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated)
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />
}

export default function App() {
  return (
    <Routes>
      {/* Auth routes */}
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
      </Route>

      {/* App routes (require auth) */}
      <Route
        element={
          <PrivateRoute>
            <MainLayout />
          </PrivateRoute>
        }
      >
        <Route index element={<HomePage />} />
        <Route path="/search" element={<SearchPage />} />
        <Route path="/library" element={<LibraryPage />} />
        <Route path="/liked" element={<LikedSongsPage />} />
        <Route path="/playlist/:id" element={<PlaylistPage />} />
        <Route path="/artist/:id" element={<ArtistPage />} />
        <Route path="/album/:id" element={<AlbumPage />} />
        <Route path="/profile" element={<ProfilePage />} />
      </Route>

      {/* Fallback */}
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  )
}
