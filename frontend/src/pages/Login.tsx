import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'
import { useAuth } from '../auth/AuthContext'
import { ApiError } from '../lib/api'

export function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [busy, setBusy] = useState(false)

  return (
    <div className="mx-auto max-w-md rounded-lg border border-slate-200 bg-white p-6">
      <h1 className="text-xl font-bold text-slate-900">AJ Systems</h1>
      <p className="mt-1 text-sm text-slate-600">Reliable daily tracking. Built right.</p>

      <form
        className="mt-5 space-y-3"
        onSubmit={async (e) => {
          e.preventDefault()
          setBusy(true)
          try {
            await login(email, password)
            toast.success('Logged in')
            navigate('/services', { replace: true })
          } catch (err: unknown) {
            if (err instanceof ApiError) toast.error(err.message)
            else toast.error('Login failed')
          } finally {
            setBusy(false)
          }
        }}
      >
        <label className="block">
          <div className="text-sm font-medium">Email</div>
          <input
            className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </label>
        <label className="block">
          <div className="text-sm font-medium">Password</div>
          <input
            className="mt-1 w-full rounded-md border border-slate-300 px-3 py-2"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </label>

        <button
          className="w-full rounded-md bg-slate-900 px-3 py-2 text-sm font-medium text-white disabled:opacity-60"
          type="submit"
          disabled={busy}
        >
          {busy ? 'Signing in…' : 'Sign in'}
        </button>
        <div className="mt-2 text-center">
          <Link to="/forgot-password" className="text-xs text-blue-600 hover:text-blue-700">
            Forgot Password?
          </Link>
        </div>
      </form>

      <div className="mt-4 text-sm text-slate-600">
        No account? <Link className="underline" to="/signup">Sign up</Link>
      </div>
    </div>
  )
}
