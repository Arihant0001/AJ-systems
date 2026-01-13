import { Navigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'
import type { ReactNode } from 'react'

export function ProtectedRoute({ children }: { children: ReactNode }) {
  const { token, loading } = useAuth()

  if (loading) return <div className="p-6">Loading…</div>
  if (!token) return <Navigate to="/login" replace />
  return <>{children}</>
}
