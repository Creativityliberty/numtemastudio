import { cn } from '@/utils/cn'
import { LayoutDashboard, Settings, Wand2, Workflow, Zap } from 'lucide-react'
import React from 'react'
import { Link, useLocation } from 'react-router-dom'

const navItems = [
  { path: '/', label: 'Dashboard', icon: LayoutDashboard },
  { path: '/agents', label: 'Agents', icon: Zap },
  { path: '/workflows', label: 'Workflows', icon: Workflow },
  { path: '/builder', label: 'Builder', icon: Wand2 },
  { path: '/settings', label: 'Settings', icon: Settings },
]

const Sidebar: React.FC = () => {
  const location = useLocation()

  return (
    <aside className="fixed left-0 top-0 h-screen w-64 border-r border-slate-700/50 bg-slate-900/50 backdrop-blur-md">
      {/* Logo */}
      <div className="flex items-center gap-3 border-b border-slate-700/50 px-6 py-6">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-indigo-500 to-pink-500">
          <span className="text-lg font-bold text-white">A</span>
        </div>
        <div>
          <h1 className="text-lg font-bold text-slate-100">Agents</h1>
          <p className="text-xs text-slate-400">Studio</p>
        </div>
      </div>

      {/* Navigation */}
      <nav className="space-y-2 px-4 py-6">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.path
          return (
            <Link
              key={item.path}
              to={item.path}
              className={cn(
                'flex items-center gap-3 rounded-lg px-4 py-2.5 transition-all duration-200',
                isActive
                  ? 'bg-indigo-600/20 text-indigo-400 shadow-lg shadow-indigo-500/10'
                  : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-100'
              )}
            >
              <Icon size={20} />
              <span className="font-medium">{item.label}</span>
            </Link>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="absolute bottom-0 left-0 right-0 border-t border-slate-700/50 bg-slate-900/50 px-6 py-4">
        <p className="text-xs text-slate-500">Nümtema Agents Studio v1.0</p>
      </div>
    </aside>
  )
}

export default Sidebar
