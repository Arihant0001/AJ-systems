import { useState } from 'react'
import { Link } from 'react-router-dom'
import { apiRequest, ApiError } from '../lib/api'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import toast from 'react-hot-toast'

export function ForgotPasswordPage() {
    const [email, setEmail] = useState('')
    const [busy, setBusy] = useState(false)
    const [sent, setSent] = useState(false)

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        setBusy(true)
        try {
            await apiRequest('/auth/forgot-password', {
                method: 'POST',
                body: { email },
            })
            // Always show success to prevent enumeration
            setSent(true)
            toast.success('Reset link sent')
        } catch (err: unknown) {
            if (err instanceof ApiError) toast.error(err.message)
            else toast.error('Something went wrong')
        } finally {
            setBusy(false)
        }
    }

    if (sent) {
        return (
            <div className="flex min-h-full flex-col justify-center py-12 sm:px-6 lg:px-8">
                <div className="sm:mx-auto sm:w-full sm:max-w-md">
                    <div className="bg-white px-4 py-8 shadow sm:rounded-lg sm:px-10 text-center">
                        <h2 className="text-xl font-bold text-slate-900 mb-2">Check your email</h2>
                        <p className="text-slate-600 mb-6">
                            If an account exists for <strong>{email}</strong>, we have sent a password reset link.
                        </p>
                        <Link to="/login">
                            <Button variant="secondary" className="w-full">
                                Back to Login
                            </Button>
                        </Link>
                    </div>
                </div>
            </div>
        )
    }

    return (
        <div className="flex min-h-full flex-col justify-center py-12 sm:px-6 lg:px-8">
            <div className="sm:mx-auto sm:w-full sm:max-w-md">
                <div className="text-center">
                    <h2 className="text-3xl font-bold tracking-tight text-slate-900">Forgot Password</h2>
                    <p className="mt-2 text-sm text-slate-600">
                        Enter your email to receive a reset link
                    </p>
                </div>

                <div className="mt-8 bg-white px-4 py-8 shadow sm:rounded-lg sm:px-10">
                    <form className="space-y-6" onSubmit={handleSubmit}>
                        <Input
                            label="Email address"
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                            autoFocus
                        />

                        <div>
                            <Button type="submit" className="w-full" loading={busy}>
                                Send Reset Link
                            </Button>
                        </div>
                    </form>

                    <div className="mt-6 text-center text-sm">
                        <Link to="/login" className="font-medium text-blue-600 hover:text-blue-500">
                            Back to Login
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    )
}
