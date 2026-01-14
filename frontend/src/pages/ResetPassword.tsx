import { useState, useMemo } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { apiRequest, ApiError } from '../lib/api'
import { Button } from '../components/ui/Button'
import { Input } from '../components/ui/Input'
import toast from 'react-hot-toast'

type PasswordStrength = {
    score: number
    label: string
    color: string
    checks: {
        length: boolean
        uppercase: boolean
        lowercase: boolean
        number: boolean
    }
}

function getPasswordStrength(password: string): PasswordStrength {
    const checks = {
        length: password.length >= 8,
        uppercase: /[A-Z]/.test(password),
        lowercase: /[a-z]/.test(password),
        number: /\d/.test(password),
    }
    
    const score = Object.values(checks).filter(Boolean).length
    
    const labels: Record<number, { label: string; color: string }> = {
        0: { label: 'Too weak', color: 'bg-red-500' },
        1: { label: 'Weak', color: 'bg-red-500' },
        2: { label: 'Fair', color: 'bg-yellow-500' },
        3: { label: 'Good', color: 'bg-blue-500' },
        4: { label: 'Strong', color: 'bg-green-500' },
    }
    
    return { score, checks, ...labels[score] }
}

export function ResetPasswordPage() {
    const [searchParams] = useSearchParams()
    const token = searchParams.get('token')

    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
    const [busy, setBusy] = useState(false)
    const [success, setSuccess] = useState(false)

    const strength = useMemo(() => getPasswordStrength(password), [password])
    const isValid = strength.score === 4 && password === confirmPassword

    if (!token) {
        return (
            <div className="flex min-h-full flex-col justify-center py-12 sm:px-6 lg:px-8">
                <div className="sm:mx-auto sm:w-full sm:max-w-md">
                    <div className="bg-white px-4 py-8 shadow sm:rounded-lg sm:px-10 text-center">
                        <div className="text-red-500 text-4xl mb-4">⚠️</div>
                        <h2 className="text-xl font-bold text-red-600">Invalid Link</h2>
                        <p className="text-slate-600 mt-2">
                            This password reset link is invalid or missing a token.
                        </p>
                        <div className="mt-6">
                            <Link to="/forgot-password">
                                <Button variant="secondary" className="w-full">
                                    Request New Link
                                </Button>
                            </Link>
                        </div>
                    </div>
                </div>
            </div>
        )
    }

    if (success) {
        return (
            <div className="flex min-h-full flex-col justify-center py-12 sm:px-6 lg:px-8">
                <div className="sm:mx-auto sm:w-full sm:max-w-md">
                    <div className="bg-white px-4 py-8 shadow sm:rounded-lg sm:px-10 text-center">
                        <div className="text-green-500 text-4xl mb-4">✓</div>
                        <h2 className="text-xl font-bold text-slate-900">Password Reset!</h2>
                        <p className="text-slate-600 mt-2">
                            Your password has been changed successfully.
                        </p>
                        <div className="mt-6">
                            <Link to="/login">
                                <Button className="w-full">
                                    Sign In
                                </Button>
                            </Link>
                        </div>
                    </div>
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
        
        if (strength.score < 4) {
            toast.error("Please meet all password requirements")
            return
        }

        setBusy(true)
        try {
            await apiRequest('/auth/reset-password', {
                method: 'POST',
                body: { token, new_password: password },
            })
            setSuccess(true)
        } catch (err: unknown) {
            if (err instanceof ApiError) {
                toast.error(err.message)
            } else {
                toast.error('Failed to reset password')
            }
        } finally {
            setBusy(false)
        }
    }

    return (
        <div className="flex min-h-full flex-col justify-center py-12 sm:px-6 lg:px-8">
            <div className="sm:mx-auto sm:w-full sm:max-w-md">
                <h2 className="text-center text-3xl font-bold tracking-tight text-slate-900">
                    Reset Password
                </h2>
                <p className="mt-2 text-center text-sm text-slate-600">
                    Enter your new password below
                </p>
            </div>

            <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
                <div className="bg-white px-4 py-8 shadow sm:rounded-lg sm:px-10">
                    <form className="space-y-5" onSubmit={handleSubmit}>
                        <div>
                            <Input
                                label="New Password"
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                            />
                            
                            {/* Password Strength Meter */}
                            {password && (
                                <div className="mt-3">
                                    <div className="flex gap-1 mb-2">
                                        {[1, 2, 3, 4].map((level) => (
                                            <div
                                                key={level}
                                                className={`h-1.5 flex-1 rounded-full transition-colors ${
                                                    level <= strength.score ? strength.color : 'bg-slate-200'
                                                }`}
                                            />
                                        ))}
                                    </div>
                                    <p className={`text-xs font-medium ${
                                        strength.score >= 4 ? 'text-green-600' : 
                                        strength.score >= 3 ? 'text-blue-600' : 
                                        strength.score >= 2 ? 'text-yellow-600' : 'text-red-600'
                                    }`}>
                                        {strength.label}
                                    </p>
                                    
                                    {/* Requirements Checklist */}
                                    <ul className="mt-2 space-y-1 text-xs">
                                        <li className={strength.checks.length ? 'text-green-600' : 'text-slate-400'}>
                                            {strength.checks.length ? '✓' : '○'} At least 8 characters
                                        </li>
                                        <li className={strength.checks.uppercase ? 'text-green-600' : 'text-slate-400'}>
                                            {strength.checks.uppercase ? '✓' : '○'} One uppercase letter
                                        </li>
                                        <li className={strength.checks.lowercase ? 'text-green-600' : 'text-slate-400'}>
                                            {strength.checks.lowercase ? '✓' : '○'} One lowercase letter
                                        </li>
                                        <li className={strength.checks.number ? 'text-green-600' : 'text-slate-400'}>
                                            {strength.checks.number ? '✓' : '○'} One number
                                        </li>
                                    </ul>
                                </div>
                            )}
                        </div>

                        <Input
                            label="Confirm Password"
                            type="password"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required
                        />
                        
                        {confirmPassword && password !== confirmPassword && (
                            <p className="text-xs text-red-500 -mt-3">
                                Passwords don't match
                            </p>
                        )}

                        <div className="pt-2">
                            <Button 
                                type="submit" 
                                className="w-full" 
                                loading={busy}
                                disabled={!isValid}
                            >
                                Reset Password
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
