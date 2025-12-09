import { cn } from '@/utils/cn'
import { Brain, Code, Database, Zap } from 'lucide-react'
import React from 'react'

export type NodeType = 'agent' | 'data' | 'logic' | 'action'

export interface WorkflowNodeProps {
  id: string
  label: string
  type: NodeType
  selected?: boolean
  onSelect?: (id: string) => void
  onDelete?: (id: string) => void
  x?: number
  y?: number
}

const nodeConfig = {
  agent: { icon: Brain, color: 'from-indigo-500 to-indigo-600', label: 'Agent' },
  data: { icon: Database, color: 'from-blue-500 to-blue-600', label: 'Data' },
  logic: { icon: Code, color: 'from-purple-500 to-purple-600', label: 'Logic' },
  action: { icon: Zap, color: 'from-pink-500 to-pink-600', label: 'Action' },
}

const WorkflowNode: React.FC<WorkflowNodeProps> = ({
  id,
  label,
  type,
  selected = false,
  onSelect,
  onDelete,
  x = 0,
  y = 0,
}) => {
  const config = nodeConfig[type]
  const Icon = config.icon

  return (
    <div
      className={cn(
        'group relative w-40 cursor-move rounded-xl border-2 bg-gradient-to-br p-4 shadow-lg transition-all duration-200',
        config.color,
        selected
          ? 'border-white shadow-2xl shadow-indigo-500/50'
          : 'border-slate-700/50 hover:border-slate-600'
      )}
      onClick={() => onSelect?.(id)}
      style={{ transform: `translate(${x}px, ${y}px)` }}
    >
      {/* Icon */}
      <div className="mb-3 flex h-12 w-12 items-center justify-center rounded-lg bg-white/10 backdrop-blur-sm">
        <Icon className="h-6 w-6 text-white" />
      </div>

      {/* Label */}
      <h3 className="mb-1 font-bold text-white">{label}</h3>
      <p className="text-xs text-white/70">{config.label}</p>

      {/* Delete Button */}
      {onDelete && (
        <button
          onClick={(e) => {
            e.stopPropagation()
            onDelete(id)
          }}
          className="absolute -right-3 -top-3 flex h-6 w-6 items-center justify-center rounded-full bg-red-500 text-white opacity-0 transition-opacity duration-200 group-hover:opacity-100"
          aria-label="Delete node"
        >
          ×
        </button>
      )}

      {/* Connection Points */}
      <div className="absolute -left-2 top-1/2 h-3 w-3 -translate-y-1/2 rounded-full border-2 border-slate-700 bg-slate-800" />
      <div className="absolute -right-2 top-1/2 h-3 w-3 -translate-y-1/2 rounded-full border-2 border-slate-700 bg-slate-800" />
    </div>
  )
}

export default WorkflowNode
