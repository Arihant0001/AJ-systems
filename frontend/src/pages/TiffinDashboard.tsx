import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import toast from 'react-hot-toast'

import { useAuth } from '../auth/AuthContext'
import { ApiError, apiRequest } from '../lib/api'
import { todayIsoDate } from '../lib/dates'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import { Modal } from '../components/ui/Modal'

type PersonStatus = {
  id: string
  name: string
  age: number
  given_count: number
  reversed_count: number
  total_tiffins: number
}

type TiffinSummary = {
  month_name: string
  total_tiffins_this_month: number
  total_active_persons: number
  today_given: number
}

type StatusOut = {
  date: string
  persons: PersonStatus[]
}

export function TiffinDashboardPage() {
  const { token, logout } = useAuth()
  const navigate = useNavigate()
  const [date, setDate] = useState(todayIsoDate())
  const [status, setStatus] = useState<StatusOut | null>(null)
  const [summary, setSummary] = useState<TiffinSummary | null>(null)
  const [loading, setLoading] = useState(false)
  const [isAddModalOpen, setIsAddModalOpen] = useState(false)

  async function refresh() {
    setLoading(true)
    try {
      const [statusOut, summaryOut] = await Promise.all([
        apiRequest<StatusOut>(`/tiffin/status?date=${date}`, { token }),
        apiRequest<TiffinSummary>(`/tiffin/summary?date=${date}`, { token }),
      ])
      setStatus(statusOut)
      setSummary(summaryOut)
    } catch (err: unknown) {
      if (err instanceof ApiError) toast.error(err.message)
      else toast.error('Failed to load status')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    refresh()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [date])

  const persons = status?.persons ?? []

  const handleLogout = () => {
    logout()
    navigate('/login', { replace: true })
  }

  return (
    <div className="min-h-screen bg-white flex flex-col">
      {/* Clean Control Header */}
      <div className="sticky top-0 z-10 border-b border-slate-200 bg-white shadow-sm">
        <div className="flex items-center justify-between px-4 py-2">
          <Input
            type="date"
            className="w-32 text-xs py-1.5"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            aria-label="Select Date"
          />
          <div className="flex items-center gap-3">
            <button
              onClick={refresh}
              disabled={loading}
              className="text-xs text-slate-600 hover:text-slate-900 disabled:text-slate-400"
            >
              {loading ? 'Loading...' : 'Refresh'}
            </button>
            <button
              className="text-xs text-slate-600 hover:text-slate-900"
              onClick={handleLogout}
            >
              Logout
            </button>
          </div>
        </div>
      </div>

      {/* Monthly Total - Compact & Focused */}
      {summary && (
        <div className="border-b border-slate-200 bg-white px-4 py-3">
          <div className="text-center">
            <div className="text-[10px] font-semibold uppercase tracking-wide text-slate-500">
              {summary.month_name}
            </div>
            <div className="mt-1 text-5xl font-bold tracking-tight text-green-600">
              {summary.total_tiffins_this_month}
            </div>
            <div className="mt-0.5 text-xs font-medium text-slate-600">
              Total Tiffins This Month
            </div>
            <div className="mt-2 text-xs text-slate-500">
              Today: <span className="font-semibold text-slate-900">{summary.today_given}</span> / {summary.total_active_persons}
            </div>
          </div>
        </div>
      )}

      {/* Action Bar */}
      <div className="border-b border-slate-100 bg-slate-50 px-4 py-2">
        <div className="flex items-center justify-center">
          <button
            onClick={() => setIsAddModalOpen(true)}
            className="text-xs text-blue-600 hover:text-blue-700 font-medium"
          >
            + Add Person
          </button>
        </div>
      </div>

      {/* People List */}
      <div className="flex-1">
        {persons.length === 0 ? (
          <EmptyState onAdd={() => setIsAddModalOpen(true)} />
        ) : (
          <div>
            {persons.map((p) => (
              <PersonRow
                key={p.id}
                person={p}
                token={token}
                date={date}
                onChanged={refresh}
              />
            ))}
          </div>
        )}
      </div>

      {/* Footer - Only Place for Branding */}
      <footer className="border-t border-slate-200 bg-slate-50 py-3 text-center">
        <p className="text-xs text-slate-500">
          © 2026 AJ Systems · Built by Arihant Jain
        </p>
      </footer>

      {/* Add Person Modal */}
      <AddPersonModal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        token={token}
        onSuccess={() => {
          setIsAddModalOpen(false)
          refresh()
        }}
      />
    </div>
  )
}


function PersonRow({
  person,
  token,
  date,
  onChanged,
}: {
  person: PersonStatus
  token: string | null
  date: string
  onChanged: () => void
}) {
  const [busy, setBusy] = useState(false)
  const netDaily = person.given_count - person.reversed_count
  const currentCount = netDaily > 0 ? netDaily : 0

  // Color coding for total tiffins (visual only)
  const getTotalColor = (total: number) => {
    if (total >= 30) return 'text-green-600 font-bold'
    if (total >= 10) return 'text-blue-600 font-semibold'
    return 'text-slate-400 font-medium'
  }

  const updateQuantity = async (newQuantity: number) => {
    if (newQuantity < 0 || newQuantity === currentCount) return
    
    setBusy(true)
    try {
      const diff = newQuantity - currentCount
      
      if (diff > 0) {
        // Add tiffins
        for (let i = 0; i < diff; i++) {
          await apiRequest('/tiffin/give', {
            method: 'POST',
            token,
            body: { person_id: person.id, date },
          })
        }
      } else {
        // Remove tiffins (undo)
        for (let i = 0; i < Math.abs(diff); i++) {
          await apiRequest('/tiffin/undo', {
            method: 'POST',
            token,
            body: { person_id: person.id, date },
          })
        }
      }
      
      toast.success(`✓ ${person.name}: ${newQuantity}`)
      onChanged()
    } catch (err: unknown) {
      if (err instanceof ApiError) toast.error(err.message)
      else toast.error('Update failed')
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="flex items-center gap-3 px-4 py-2.5 hover:bg-slate-50 border-b border-slate-100">
      {/* Name & Status */}
      <div className="flex-1 min-w-0">
        <Link to={`/services/tiffin/person/${person.id}`} className="block">
          <div className="flex items-center gap-2">
            <span className="font-semibold text-slate-900 text-sm">{person.name}</span>
            <span className={`text-[10px] ${getTotalColor(person.total_tiffins)}`}>
              {person.total_tiffins}
            </span>
          </div>
          <div className="flex items-center gap-1.5 mt-0.5">
            <span className={`inline-flex h-1.5 w-1.5 rounded-full ${currentCount > 0 ? 'bg-green-500' : 'bg-slate-400'}`} />
            <span className="text-[11px] text-slate-500">
              {currentCount > 0 ? `Given (${currentCount})` : 'Not Given'}
            </span>
          </div>
        </Link>
      </div>

      {/* Today Stepper */}
      <div className="shrink-0 flex items-center gap-1.5">
        <span className="text-[11px] text-slate-500 font-medium">Today:</span>
        <div className="flex items-center border border-slate-300 rounded">
          <button
            onClick={() => updateQuantity(currentCount - 1)}
            disabled={busy || currentCount <= 0}
            className="w-7 h-8 flex items-center justify-center text-slate-600 hover:bg-slate-100 disabled:opacity-25 disabled:cursor-not-allowed"
          >
            −
          </button>
          <div className="w-10 h-8 flex items-center justify-center text-sm font-semibold text-slate-900 border-x border-slate-300 bg-white">
            {currentCount}
          </div>
          <button
            onClick={() => updateQuantity(currentCount + 1)}
            disabled={busy || currentCount >= 99}
            className="w-7 h-8 flex items-center justify-center text-slate-600 hover:bg-slate-100 disabled:opacity-25 disabled:cursor-not-allowed"
          >
            +
          </button>
        </div>
      </div>
    </div>
  )
}


function AddPersonModal({
  isOpen,
  onClose,
  token,
  onSuccess,
}: {
  isOpen: boolean
  onClose: () => void
  token: string | null
  onSuccess: () => void
}) {
  const [name, setName] = useState('')
  const [age, setAge] = useState('')
  const [busy, setBusy] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setBusy(true)

    const parsedAge = Number(age)
    if (!name.trim() || !age || isNaN(parsedAge)) {
      toast.error('Please enter valid name and age')
      setBusy(false)
      return
    }

    try {
      await apiRequest('/persons', {
        method: 'POST',
        token,
        body: { name: name.trim(), age: parsedAge },
      })
      toast.success('Person added successfully')
      setName('')
      setAge('')
      onSuccess()
    } catch (err: unknown) {
      if (err instanceof ApiError) toast.error(err.message)
      else toast.error('Failed to add person')
    } finally {
      setBusy(false)
    }
  }

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Add New Person">
      <form onSubmit={handleSubmit} className="mt-4 flex flex-col gap-4">
        <Input
          label="Full Name"
          placeholder="e.g. John Doe"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <Input
          label="Age"
          type="number"
          placeholder="e.g. 35"
          value={age}
          onChange={(e) => setAge(e.target.value)}
          required
          min={0}
          max={150}
        />
        <div className="mt-2 flex justify-end gap-3">
          <Button type="button" variant="ghost" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" loading={busy}>
            Add Person
          </Button>
        </div>
      </form>
    </Modal>
  )
}


function EmptyState({ onAdd }: { onAdd: () => void }) {
  return (
    <div className="flex flex-col items-center justify-center px-4 py-16 text-center">
      <div className="text-slate-400 mb-3">
        <svg className="h-12 w-12 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
          />
        </svg>
      </div>
      <h3 className="text-base font-medium text-slate-900">No persons found</h3>
      <p className="mt-1 text-sm text-slate-500">Add people to start tracking</p>
      <button
        onClick={onAdd}
        className="mt-4 h-10 px-5 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md"
      >
        Add First Person
      </button>
    </div>
  )
}


