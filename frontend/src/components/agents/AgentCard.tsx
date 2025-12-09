import Button from '@/components/common/Button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/common/Card'
import { Copy, Edit2, Trash2, Zap } from 'lucide-react'
import React from 'react'

export interface AgentCardProps {
  id: string
  name: string
  description: string
  type: string
  status: 'active' | 'inactive' | 'error'
  onEdit?: (id: string) => void
  onDelete?: (id: string) => void
  onDuplicate?: (id: string) => void
}

const statusConfig = {
  active: { color: 'text-green-400', bg: 'bg-green-500/10' },
  inactive: { color: 'text-slate-400', bg: 'bg-slate-500/10' },
  error: { color: 'text-red-400', bg: 'bg-red-500/10' },
}

const AgentCard: React.FC<AgentCardProps> = ({
  id,
  name,
  description,
  type,
  status,
  onEdit,
  onDelete,
  onDuplicate,
}) => {
  const statusStyle = statusConfig[status]

  return (
    <Card hoverable gradient className="group">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-indigo-500/20">
              <Zap className="h-5 w-5 text-indigo-400" />
            </div>
            <div>
              <CardTitle className="text-lg">{name}</CardTitle>
              <CardDescription className="text-xs uppercase tracking-wider">
                {type}
              </CardDescription>
            </div>
          </div>
          <div className={`rounded-full px-3 py-1 text-xs font-medium ${statusStyle.bg} ${statusStyle.color}`}>
            {status}
          </div>
        </div>
      </CardHeader>

      <CardContent>
        <p className="mb-4 text-sm text-slate-300">{description}</p>

        <div className="flex gap-2 opacity-0 transition-opacity duration-200 group-hover:opacity-100">
          {onEdit && (
            <Button
              size="sm"
              variant="secondary"
              icon={<Edit2 size={16} />}
              onClick={() => onEdit(id)}
            >
              Edit
            </Button>
          )}
          {onDuplicate && (
            <Button
              size="sm"
              variant="outline"
              icon={<Copy size={16} />}
              onClick={() => onDuplicate(id)}
            >
              Duplicate
            </Button>
          )}
          {onDelete && (
            <Button
              size="sm"
              variant="danger"
              icon={<Trash2 size={16} />}
              onClick={() => onDelete(id)}
            >
              Delete
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  )
}

export default AgentCard
