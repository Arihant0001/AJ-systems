/* eslint-disable react-refresh/only-export-components */
import React, { createContext, useContext, useEffect, useMemo, useState } from 'react'
import { apiRequest } from '../lib/api'
import { clearToken, getToken, setToken } from '../lib/storage'
import type { User } from './types'

type AuthContextValue = {
  token: string | null
  user: User | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  signup: (name: string, email: string, password: string) => Promise<void>
  logout: () => void
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setTokenState] = useState<string | null>(() => getToken())
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false

    async function bootstrap() {
      if (!token) {
        setLoading(false)
        return
      }
      try {
        const me = await apiRequest<User>('/auth/me', { token })
        if (!cancelled) setUser(me)
      } catch {
        clearToken()
        if (!cancelled) {
          setTokenState(null)
          setUser(null)
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    }

    bootstrap()
    return () => {
      cancelled = true
    }
  }, [token])

  const value = useMemo<AuthContextValue>(
    () => ({
      token,
      user,
      loading,
      login: async (email, password) => {
        const out = await apiRequest<{ access_token: string; token_type: string }>('/auth/login', {
          method: 'POST',
          body: { email, password },
        })
        setToken(out.access_token)
        setTokenState(out.access_token)
        const me = await apiRequest<User>('/auth/me', { token: out.access_token })
        setUser(me)
      },
      signup: async (name, email, password) => {
        await apiRequest('/auth/signup', {
          method: 'POST',
          body: { name, email, password },
        })
        await (async () => {
          const out = await apiRequest<{ access_token: string; token_type: string }>('/auth/login', {
            method: 'POST',
            body: { email, password },
          })
          setToken(out.access_token)
          setTokenState(out.access_token)
          const me = await apiRequest<User>('/auth/me', { token: out.access_token })
          setUser(me)
        })()
      },
      logout: () => {
        clearToken()
        setTokenState(null)
        setUser(null)
      },
    }),
    [token, user, loading],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
