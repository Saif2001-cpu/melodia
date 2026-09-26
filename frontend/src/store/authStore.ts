import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User } from '@/types'

interface AuthState {
  user: User | null
  accessToken: string | null
  isAuthenticated: boolean

  setAuth: (user: User, token: string) => void
  setUser: (user: User) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      isAuthenticated: false,

      setAuth: (user, accessToken) => {
        localStorage.setItem('access_token', accessToken)
        set({ user, accessToken, isAuthenticated: true })
      },

      setUser: (user) => set({ user }),

      logout: () => {
        localStorage.removeItem('access_token')
        set({ user: null, accessToken: null, isAuthenticated: false })
      },
    }),
    {
      name: 'melodia-auth',
      partialize: (state) => ({
        user: state.user,
        accessToken: state.accessToken,
        isAuthenticated: state.isAuthenticated,
      }),
      // After rehydrating from localStorage, sync token to localStorage so
      // the Axios interceptor can pick it up on page load.
      onRehydrateStorage: () => (state) => {
        if (state?.accessToken) {
          localStorage.setItem('access_token', state.accessToken)
        }
      },
    },
  ),
)
