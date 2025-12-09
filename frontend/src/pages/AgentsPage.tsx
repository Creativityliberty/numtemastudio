import AgentCard from '@/components/agents/AgentCard'
import Button from '@/components/common/Button'
import { Card, CardContent } from '@/components/common/Card'
import Input from '@/components/common/Input'
import { Plus, Search } from 'lucide-react'
import React, { useState } from 'react'

const AgentsPage: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [filterType, setFilterType] = useState<string>('all')

  const agents = [
    { id: '1', name: 'Research Agent', description: 'Researches topics', type: 'Research', status: 'active' as const },
    { id: '2', name: 'Writer Agent', description: 'Writes content', type: 'Writer', status: 'active' as const },
    { id: '3', name: 'Coder Agent', description: 'Writes code', type: 'Coder', status: 'active' as const },
    { id: '4', name: 'Reviewer Agent', description: 'Reviews content', type: 'Reviewer', status: 'inactive' as const },
    { id: '5', name: 'Analyzer Agent', description: 'Analyzes data', type: 'Analyzer', status: 'active' as const },
    { id: '6', name: 'Translator Agent', description: 'Translates text', type: 'Translator', status: 'error' as const },
  ]

  const agentTypes = ['all', 'Research', 'Writer', 'Coder', 'Reviewer', 'Analyzer', 'Translator']

  const filteredAgents = agents.filter((agent) => {
    const matchesSearch = agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      agent.description.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesType = filterType === 'all' || agent.type === filterType
    return matchesSearch && matchesType
  })

  return (
    <div className="space-y-8 p-8">
      {/* Header */}
      <div className="flex flex-col items-start justify-between gap-4 md:flex-row md:items-center">
        <div>
          <h1 className="text-4xl font-bold text-slate-100">Agents</h1>
          <p className="mt-2 text-slate-400">Manage and create AI agents</p>
        </div>
        <Button variant="primary" size="lg" icon={<Plus size={20} />}>
          Create Agent
        </Button>
      </div>

      {/* Filters */}
      <Card>
        <CardContent className="space-y-4 pt-6">
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <Input
              label="Search agents"
              placeholder="Search by name or description..."
              icon={<Search size={18} />}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <div>
              <label className="mb-2 block text-sm font-medium text-slate-200">Type</label>
              <select
                value={filterType}
                onChange={(e) => setFilterType(e.target.value)}
                className="w-full rounded-lg border border-slate-600 bg-slate-800/50 px-4 py-2 text-slate-100 transition-all focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
              >
                {agentTypes.map((type) => (
                  <option key={type} value={type}>
                    {type.charAt(0).toUpperCase() + type.slice(1)}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Agents Grid */}
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
        {filteredAgents.map((agent) => (
          <AgentCard
            key={agent.id}
            {...agent}
            onEdit={() => console.log('Edit', agent.id)}
            onDelete={() => console.log('Delete', agent.id)}
            onDuplicate={() => console.log('Duplicate', agent.id)}
          />
        ))}
      </div>

      {filteredAgents.length === 0 && (
        <Card className="text-center">
          <CardContent className="py-12">
            <p className="text-slate-400">No agents found. Try adjusting your search or filters.</p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}

export default AgentsPage
