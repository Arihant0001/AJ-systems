import { useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { apiRequest, ApiError } from '../lib/api'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import toast from 'react-hot-toast'

export function ResetPasswordPage() {
    const [searchParams] = useSearchParams()
    const token = searchParams.get('token')
    const navigate = useNavigate()

    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [busy, setBusy] = useState(false)

    if (!token) {
        return (
            <div className="p-12 text-center">
                <h2 className="text-xl font-bold text-red-600">Invalid Link</h2>
                <p className="text-slate-600 mt-2">This password reset link is invalid or missing a token.</p>
                <div className="mt-4">
                    <Link to="/login" className="text-blue-600 hover:underline">Return to Login</Link>
                </div>
            </div>
        )
    }

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault()
        if (password !== confirmPassword) {
            toast.error("Passwords don't match")
            return
        }
        if (password.length < 8) {
            toast.error("Password must be at least 8 characters")
            return
        }

        setBusy(true)
        try {
            await apiRequest('/auth/reset-password', {
                method: 'POST',
                body: { token, new_password: password },
            })
            toast.success('Password reset successfully')
            navigate('/login')
        } catch (err: unknown) {
            if (err instanceof ApiError) toast.error(err.message)
            else toast.error('Failed to reset password')
        } finally {
            setBusy(false)
        }
    }

    return (
        <div className="flex min-h-full flex-col justify-center py-12 sm:px-6 lg:px-8">
            <div className="sm:mx-auto sm:w-full sm:max-w-md">
                <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-slate-900">
                    Reset Password
                </h2>
                <p className="mt-2 text-center text-sm text-slate-600">
                    Enter your new password below
                </p>
            </div>

            <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
                <div className="bg-white px-4 py-8 shadow sm:rounded-lg sm:px-10">
                    <form className="space-y-6" onSubmit={handleSubmit}>
                        <Input
                            label="New Password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            minLength={8}
                        />

                        <Input
                            label="Confirm Password"
                            type="password"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required
                            minLength={8}
                        />

                        <div>
                            <Button type="submit" className="w-full" loading={busy}>
                                Reset Password
                            </Button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    )
}
