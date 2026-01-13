import { Navigate, Route, Routes } from 'react-router-dom'

import { ProtectedRoute } from './components/ProtectedRoute'
import { AppLayout } from './components/AppLayout'
import { LoginPage } from './pages/Login'
import { SignupPage } from './pages/Signup'
import { DashboardHome } from './pages/DashboardHome'
import { TiffinDashboardPage } from './pages/TiffinDashboard'
import { PersonHistoryPage } from './pages/PersonHistory'
import { ForgotPasswordPage } from './pages/ForgotPassword'
import { ResetPasswordPage } from './pages/ResetPassword'

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/services" replace />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/signup" element={<SignupPage />} />
      <Route path="/forgot-password" element={<ForgotPasswordPage />} />
      <Route path="/reset-password" element={<ResetPasswordPage />} />

      <Route
        element={
          <ProtectedRoute>
            <AppLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/services" element={<DashboardHome />} />
        <Route path="/services/tiffin" element={<TiffinDashboardPage />} />
        <Route path="/services/tiffin/person/:personId" element={<PersonHistoryPage />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
