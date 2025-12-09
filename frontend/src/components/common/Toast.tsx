import { cn } from '@/utils/cn'
import { AlertCircle, CheckCircle, Info, X } from 'lucide-react'
import React, { useEffect } from 'react'

export type ToastType = 'success' | 'error' | 'warning' | 'info'

export interface ToastProps {
  id: string
  type: ToastType
  title: string
  description?: string
  duration?: number
  onClose: (id: string) => void
}

const typeConfig = {
  success: {
    icon: CheckCircle,
    bgColor: 'bg-green-900/20',
    borderColor: 'border-green-700/50',
    textColor: 'text-green-100',
    iconColor: 'text-green-500',
  },
  error: {
    icon: AlertCircle,
    bgColor: 'bg-red-900/20',
    borderColor: 'border-red-700/50',
    textColor: 'text-red-100',
    iconColor: 'text-red-500',
  },
  warning: {
    icon: AlertCircle,
    bgColor: 'bg-yellow-900/20',
    borderColor: 'border-yellow-700/50',
    textColor: 'text-yellow-100',
    iconColor: 'text-yellow-500',
  },
  info: {
    icon: Info,
    bgColor: 'bg-blue-900/20',
    borderColor: 'border-blue-700/50',
    textColor: 'text-blue-100',
    iconColor: 'text-blue-500',
  },
}

const Toast: React.FC<ToastProps> = ({
  id,
  type,
  title,
  description,
  duration = 5000,
  onClose,
}) => {
  const config = typeConfig[type]
  const Icon = config.icon

  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => onClose(id), duration)
      return () => clearTimeout(timer)
    }
  }, [id, duration, onClose])

  return (
    <div
      className={cn(
        'animate-slide-in-up rounded-lg border px-4 py-3 shadow-lg',
        config.bgColor,
        config.borderColor
      )}
    >
      <div className="flex items-start gap-3">
        <Icon className={cn('mt-0.5 h-5 w-5 flex-shrink-0', config.iconColor)} />
        <div className="flex-1">
          <p className={cn('font-medium', config.textColor)}>{title}</p>
          {description && (
            <p className={cn('mt-1 text-sm opacity-90', config.textColor)}>
              {description}
            </p>
          )}
        </div>
        <button
          onClick={() => onClose(id)}
          className={cn(
            'flex-shrink-0 rounded-lg p-1 transition-colors hover:bg-white/10',
            config.textColor
          )}
          aria-label="Close notification"
        >
          <X size={18} />
        </button>
      </div>
    </div>
  )
}

export default Toast
