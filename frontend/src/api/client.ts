import axios, { type AxiosError, type InternalAxiosRequestConfig } from 'axios'
import type { ApiError } from '@/types'

export const apiClient = axios.create({
  baseURL: (import.meta.env.VITE_API_URL ?? '') + '/api/v1',
  timeout: 15_000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// ── Request interceptor — inject JWT ─────────────────────────────────────────
apiClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// ── Response interceptor — handle 401 ────────────────────────────────────────
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError<ApiError>) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  },
)

export function extractApiError(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const data = error.response?.data as ApiError | undefined
    return data?.message ?? error.message
  }
  if (error instanceof Error) return error.message
  return 'An unexpected error occurred'
}
