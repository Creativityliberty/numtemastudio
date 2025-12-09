import Sidebar from '@/components/common/Sidebar'
import Toast from '@/components/common/Toast'
import { useToast } from '@/hooks/useToast'
import React from 'react'
import { Outlet } from 'react-router-dom'

const MainLayout: React.FC = () => {
  const { toasts, removeToast } = useToast()

  return (
    <div className="flex h-screen bg-slate-900">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content */}
      <main className="ml-64 flex-1 overflow-auto">
        <Outlet />
      </main>

      {/* Toast Container */}
      <div className="fixed bottom-6 right-6 z-40 flex flex-col gap-3">
        {toasts.map((toast) => (
          <Toast
            key={toast.id}
            id={toast.id}
            type={toast.type}
            title={toast.title}
            description={toast.description}
            duration={toast.duration}
            onClose={removeToast}
          />
        ))}
      </div>
    </div>
  )
}

export default MainLayout
