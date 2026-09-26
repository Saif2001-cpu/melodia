import { apiClient } from './client'
import type { AuthTokens, LoginRequest, RegisterRequest, User } from '@/types'

export const authApi = {
  login: async (data: LoginRequest): Promise<AuthTokens> => {
    const resp = await apiClient.post<AuthTokens>('/auth/login', data)
    return resp.data
  },

  register: async (data: RegisterRequest): Promise<User> => {
    const resp = await apiClient.post<User>('/auth/register', data)
    return resp.data
  },

  logout: async (): Promise<void> => {
    // Logout is client-side only — the backend has no logout endpoint.
    // The client simply discards the token (handled by authStore.logout()).
  },

  me: async (): Promise<User> => {
    const resp = await apiClient.get<User>('/auth/me')
    return resp.data
  },

  refreshToken: async (): Promise<AuthTokens> => {
    const resp = await apiClient.post<AuthTokens>('/auth/refresh')
    return resp.data
  },
}
