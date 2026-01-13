import { useEffect, useMemo, useState } from 'react'
import { Link, useParams, useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'

import { useAuth } from '../auth/AuthContext'
import { ApiError, apiRequest } from '../lib/api'

type Log = {
  id: string
  person_id: string
  date: string
  action: 'GIVEN' | 'REVERSED'
  created_at: string
}

type PersonStatus = {
  id: string
  name: string
  age: number
  given_count: number
  reversed_count: number
  total_tiffins: number
}

type PersonOut = {
  id: string
  name: string
  age: number
  created_at: string
}

export function PersonHistoryPage() {
  const { token, logout } = useAuth()
  const navigate = useNavigate()
  const { personId } = useParams()
  const [logs, setLogs] = useState<Log[]>([])
  const [person, setPerson] = useState<PersonStatus | null>(null)
  const [loading, setLoading] = useState(false)
  const [pdfLoading, setPdfLoading] = useState(false)

  useEffect(() => {
    let cancelled = false
    async function load() {
      if (!personId) return
      setLoading(true)
      try {
        const out = await apiRequest<Log[]>(`/tiffin/history/${personId}`, { token })
        if (!cancelled) setLogs(out)

        const people = await apiRequest<PersonOut[]>('/persons', { token })
        const found = people.find((p) => p.id === personId)
        if (!cancelled) {
          setPerson(
            found
              ? { id: found.id, name: found.name, age: found.age, given_count: 0, reversed_count: 0, total_tiffins: 0 }
              : null,
          )
        }
      } catch (err: unknown) {
        if (err instanceof ApiError) toast.error(err.message)
        else toast.error('Failed to load history')
      } finally {
        setLoading(false)
      }
    }
    load()
    return () => {
      cancelled = true
    }
  }, [personId, token])

  const total = useMemo(() => logs.reduce((acc, l) => acc + (l.action === 'GIVEN' ? 1 : -1), 0), [logs])

  const handleDownloadPdf = async () => {
    if (!personId) return
    setPdfLoading(true)
    try {
      const blob = await apiRequest<Blob>(`/tiffin/pdf/${personId}`, {
        token,
        responseType: 'blob',
      })
      const url = URL.createObjectURL(blob)
      window.open(url, '_blank')
      setTimeout(() => URL.revokeObjectURL(url), 60_000)
    } catch (err: unknown) {
      if (err instanceof ApiError) toast.error(err.message)
      else toast.error('Failed to generate PDF')
    } finally {
      setPdfLoading(false)
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/login', { replace: true })
  }

  if (loading && !person) {
    return <div className="p-8 text-center text-slate-500">Loading history...</div>
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Sticky Header */}
      <div className="sticky top-0 z-10 border-b border-slate-200 bg-white">
        <div className="flex items-center justify-between px-4 py-3">
          <h1 className="text-lg font-bold text-slate-900">Person History</h1>
          <button
            className="text-xs text-slate-600 hover:text-slate-900"
            onClick={handleLogout}
          >
            Logout
          </button>
        </div>
        
        {/* Person Info Strip */}
        {person && (
          <div className="border-t border-slate-100 bg-slate-50 px-4 py-2">
            <div className="flex items-center justify-between text-sm">
              <div>
                <span className="font-medium text-slate-900">{person.name}</span>
                <span className="text-slate-500"> • {person.age} years</span>
              </div>
              <div>
                <span className="text-slate-500">Total: </span>
                <span className="font-bold text-slate-900">{total}</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Action Bar */}
      <div className="border-b border-slate-100 bg-white px-4 py-2 flex items-center justify-between">
        <Link to="/services/tiffin" className="text-sm text-blue-600 hover:text-blue-700">
          ← Back
        </Link>
        <button
          onClick={handleDownloadPdf}
          disabled={pdfLoading}
          className="text-sm font-medium text-blue-600 hover:text-blue-700 disabled:text-slate-400"
        >
          {pdfLoading ? 'Generating...' : 'Download PDF'}
        </button>
      </div>

      {/* History List */}
      <div className="flex-1">
        {logs.length === 0 ? (
          <div className="flex flex-col items-center justify-center px-4 py-16 text-center">
            <div className="text-slate-400 mb-3">
              <svg className="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h3 className="text-base font-medium text-slate-900">No history yet</h3>
            <p className="mt-1 text-sm text-slate-500">Records will appear here</p>
          </div>
        ) : (
          <div className="divide-y divide-slate-100">
            {logs.map((l) => (
              <div key={l.id} className="flex items-center justify-between px-4 py-3 hover:bg-slate-50">
                <div className="flex-1">
                  <div className="font-medium text-slate-900 text-sm">
                    {new Date(l.date).toLocaleDateString(undefined, {
                      weekday: 'short',
                      month: 'short',
                      day: 'numeric',
                      year: 'numeric',
                    })}
                  </div>
                  <div className="text-xs text-slate-500 mt-0.5">
                    {new Date(l.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
                <div className="shrink-0">
                  <span
                    className={`inline-flex items-center px-2.5 py-1 text-xs font-medium rounded ${
                      l.action === 'GIVEN'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-orange-100 text-orange-800'
                    }`}
                  >
                    {l.action === 'GIVEN' ? 'Given' : 'Reversed'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-slate-50 py-3 text-center">
        <p className="text-xs text-slate-500">
          © 2026 AJ Systems · Built by Arihant Jain
        </p>
      </footer>
    </div>
  )
}
