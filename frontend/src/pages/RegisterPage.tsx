import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import { Loader2, Mail, Lock, User } from 'lucide-react'

import { authApi } from '@/api/auth'
import { extractApiError } from '@/api/client'
import { useAuthStore } from '@/store/authStore'
import type { RegisterRequest } from '@/types'

export function RegisterPage() {
  const navigate = useNavigate()
  const setAuth = useAuthStore((state) => state.setAuth)
  const [error, setError] = useState<string | null>(null)
  
  const [formData, setFormData] = useState<RegisterRequest>({
    email: '',
    username: '',
    password: '',
  })

  const registerMutation = useMutation({
    mutationFn: async (data: RegisterRequest) => {
      // 1. Register user
      await authApi.register(data)
      
      // 2. Automatically login after register
      const tokens = await authApi.login({ email: data.email, password: data.password })
      localStorage.setItem('access_token', tokens.access_token)
      
      // 3. Get profile
      const user = await authApi.me()
      return { user, tokens }
    },
    onSuccess: ({ user, tokens }) => {
      setAuth(user, tokens.access_token)
      navigate('/')
    },
    onError: (err) => {
      setError(extractApiError(err))
      localStorage.removeItem('access_token')
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    registerMutation.mutate(formData)
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }))
  }

  return (
    <div className="flex flex-col gap-6">
      <div className="text-center">
        <h2 className="text-2xl font-semibold text-white">Create Account</h2>
        <p className="text-surface-400 text-sm mt-1">Join Melodia and start listening</p>
      </div>

      {error && (
        <div className="bg-red-500/10 border border-red-500/50 text-red-500 text-sm rounded-lg p-3 text-center">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div className="space-y-1">
          <label className="text-sm font-medium text-surface-300" htmlFor="email">
            Email
          </label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-surface-500" />
            <input
              id="email"
              name="email"
              type="email"
              required
              placeholder="name@example.com"
              value={formData.email}
              onChange={handleChange}
              className="w-full bg-surface-900 border border-surface-700 rounded-lg py-2.5 pl-10 pr-4 text-white placeholder:text-surface-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            />
          </div>
        </div>

        <div className="space-y-1">
          <label className="text-sm font-medium text-surface-300" htmlFor="username">
            Username
          </label>
          <div className="relative">
            <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-surface-500" />
            <input
              id="username"
              name="username"
              type="text"
              required
              minLength={3}
              maxLength={50}
              placeholder="melodia_fan"
              value={formData.username}
              onChange={handleChange}
              className="w-full bg-surface-900 border border-surface-700 rounded-lg py-2.5 pl-10 pr-4 text-white placeholder:text-surface-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            />
          </div>
        </div>

        <div className="space-y-1">
          <label className="text-sm font-medium text-surface-300" htmlFor="password">
            Password
          </label>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-surface-500" />
            <input
              id="password"
              name="password"
              type="password"
              required
              minLength={8}
              placeholder="••••••••"
              value={formData.password}
              onChange={handleChange}
              className="w-full bg-surface-900 border border-surface-700 rounded-lg py-2.5 pl-10 pr-4 text-white placeholder:text-surface-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={registerMutation.isPending}
          className="w-full bg-primary-600 hover:bg-primary-500 text-white font-medium py-2.5 rounded-lg transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed mt-2"
        >
          {registerMutation.isPending && <Loader2 className="w-5 h-5 animate-spin" />}
          Sign Up
        </button>
      </form>

      <p className="text-center text-sm text-surface-400">
        Already have an account?{' '}
        <Link to="/login" className="text-primary-400 hover:text-primary-300 transition-colors">
          Log in
        </Link>
      </p>
    </div>
  )
}
