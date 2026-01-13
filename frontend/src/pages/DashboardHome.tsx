import { useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

export function DashboardHome() {
    const navigate = useNavigate()
    const { logout } = useAuth()

    const handleLogout = () => {
        logout()
        navigate('/login', { replace: true })
    }

    return (
        <div className="min-h-screen bg-white flex flex-col">
            {/* Clean Control Header */}
            <div className="sticky top-0 z-10 border-b border-slate-200 bg-white shadow-sm">
                <div className="flex items-center justify-end px-4 py-2">
                    <button
                        className="text-xs text-slate-600 hover:text-slate-900"
                        onClick={handleLogout}
                    >
                        Logout
                    </button>
                </div>
            </div>

            {/* Main Content */}
            <div className="flex-1 px-4 py-6">
                <div className="mb-6">
                    <h2 className="text-xl font-bold text-slate-900">Available Services</h2>
                    <p className="mt-1 text-sm text-slate-600">
                        Select a service to get started
                    </p>
                </div>

                <div className="space-y-3">
                    {/* Tiffin Service - Active */}
                    <button
                        onClick={() => navigate('/services/tiffin')}
                        className="w-full flex items-center justify-between p-4 border border-slate-200 bg-white hover:bg-slate-50 active:bg-slate-100 rounded-lg"
                    >
                        <div className="flex items-center gap-3">
                            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-orange-100 text-orange-600">
                                <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
                                    />
                                </svg>
                            </div>
                            <div className="text-left">
                                <div className="font-medium text-slate-900">Tiffin Management</div>
                                <div className="text-xs text-slate-500">Track daily distribution</div>
                            </div>
                        </div>
                        <span className="text-xs font-medium text-green-600">Active</span>
                    </button>

                    {/* Coming Soon Services */}
                    <div className="opacity-50 flex items-center justify-between p-4 border border-slate-200 bg-slate-50 rounded-lg">
                        <div className="flex items-center gap-3">
                            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-slate-100 text-slate-400">
                                <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"
                                    />
                                </svg>
                            </div>
                            <div className="text-left">
                                <div className="font-medium text-slate-700">Laundry Service</div>
                                <div className="text-xs text-slate-500">Coming soon</div>
                            </div>
                        </div>
                    </div>

                    <div className="opacity-50 flex items-center justify-between p-4 border border-slate-200 bg-slate-50 rounded-lg">
                        <div className="flex items-center gap-3">
                            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-slate-100 text-slate-400">
                                <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                                    <path
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                                    />
                                </svg>
                            </div>
                            <div className="text-left">
                                <div className="font-medium text-slate-700">Attendance</div>
                                <div className="text-xs text-slate-500">Coming soon</div>
                            </div>
                        </div>
                    </div>
                </div>
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
