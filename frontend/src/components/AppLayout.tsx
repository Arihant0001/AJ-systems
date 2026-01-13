import { Outlet } from 'react-router-dom'

export function AppLayout() {
  return (
    <div className="flex min-h-screen flex-col bg-white">
      <main className="flex-1">
        <Outlet />
      </main>
    </div>
  )
}
