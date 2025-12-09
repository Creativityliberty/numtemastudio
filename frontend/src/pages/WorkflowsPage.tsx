import Button from '@/components/common/Button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card'
import Input from '@/components/common/Input'
import WorkflowNode from '@/components/workflows/WorkflowNode'
import { Edit2, Play, Plus, Search, Trash2 } from 'lucide-react'
import React, { useState } from 'react'

const WorkflowsPage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedWorkflow, setSelectedWorkflow] = useState<string | null>(null)

  const workflows = [
    { id: '1', name: 'Research & Write', description: 'Research topic then write article', nodes: 3, status: 'active' as const },
    { id: '2', name: 'Code Review Pipeline', description: 'Code generation and review', nodes: 4, status: 'active' as const },
    { id: '3', name: 'Content Analysis', description: 'Analyze and summarize content', nodes: 2, status: 'inactive' as const },
    { id: '4', name: 'Multi-Agent Collaboration', description: 'Complex multi-agent workflow', nodes: 5, status: 'active' as const },
  ]

  const filteredWorkflows = workflows.filter((w) =>
    w.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    w.description.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="space-y-8 p-8">
      {/* Header */}
      <div className="flex flex-col items-start justify-between gap-4 md:flex-row md:items-center">
        <div>
          <h1 className="text-4xl font-bold text-slate-100">Workflows</h1>
          <p className="mt-2 text-slate-400">Create and manage AI workflows</p>
        </div>
        <Button variant="primary" size="lg" icon={<Plus size={20} />}>
          Create Workflow
        </Button>
      </div>

      {/* Search */}
      <Card>
        <CardContent className="pt-6">
          <Input
            label="Search workflows"
            placeholder="Search by name or description..."
            icon={<Search size={18} />}
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </CardContent>
      </Card>

      {/* Workflows List */}
      <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* List */}
        <div className="lg:col-span-2 space-y-4">
          {filteredWorkflows.map((workflow) => (
            <Card
              key={workflow.id}
              hoverable
              className={selectedWorkflow === workflow.id ? 'border-indigo-500' : ''}
              onClick={() => setSelectedWorkflow(workflow.id)}
            >
              <CardContent className="pt-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="text-lg font-bold text-slate-100">{workflow.name}</h3>
                    <p className="mt-1 text-sm text-slate-400">{workflow.description}</p>
                    <div className="mt-3 flex items-center gap-4">
                      <span className="text-xs text-slate-500">{workflow.nodes} nodes</span>
                      <span className={`text-xs font-medium ${workflow.status === 'active' ? 'text-green-400' : 'text-slate-400'}`}>
                        {workflow.status}
                      </span>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <Button size="icon" variant="secondary" title="Run workflow">
                      <Play size={18} />
                    </Button>
                    <Button size="icon" variant="secondary" title="Edit workflow">
                      <Edit2 size={18} />
                    </Button>
                    <Button size="icon" variant="danger" title="Delete workflow">
                      <Trash2 size={18} />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}

          {filteredWorkflows.length === 0 && (
            <Card>
              <CardContent className="py-12 text-center">
                <p className="text-slate-400">No workflows found. Create one to get started.</p>
              </CardContent>
            </Card>
          )}
        </div>

        {/* Preview */}
        <div>
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Workflow Preview</CardTitle>
            </CardHeader>
            <CardContent>
              {selectedWorkflow ? (
                <div className="space-y-4">
                  <div className="flex flex-col gap-3">
                    <WorkflowNode id="1" label="Start" type="agent" />
                    <div className="text-center text-slate-500">↓</div>
                    <WorkflowNode id="2" label="Process" type="logic" />
                    <div className="text-center text-slate-500">↓</div>
                    <WorkflowNode id="3" label="Output" type="action" />
                  </div>
                </div>
              ) : (
                <p className="text-center text-slate-400">Select a workflow to preview</p>
              )}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default WorkflowsPage
