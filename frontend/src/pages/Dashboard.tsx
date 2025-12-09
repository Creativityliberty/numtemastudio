import AgentCard from '@/components/agents/AgentCard'
import Button from '@/components/common/Button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card'
import { BarChart3, TrendingUp, Workflow, Zap } from 'lucide-react'
import React from 'react'

const Dashboard: React.FC = () => {
  // Mock data
  const stats = [
    { label: 'Total Agents', value: '12', icon: Zap, color: 'from-indigo-500 to-indigo-600' },
    { label: 'Active Workflows', value: '8', icon: Workflow, color: 'from-blue-500 to-blue-600' },
    { label: 'Executions Today', value: '156', icon: TrendingUp, color: 'from-green-500 to-green-600' },
    { label: 'Success Rate', value: '98.5%', icon: BarChart3, color: 'from-pink-500 to-pink-600' },
  ]

  const recentAgents = [
    {
      id: '1',
      name: 'Research Agent',
      description: 'Researches topics and gathers information',
      type: 'Research',
      status: 'active' as const,
    },
    {
      id: '2',
      name: 'Writer Agent',
      description: 'Writes and edits content',
      type: 'Writer',
      status: 'active' as const,
    },
    {
      id: '3',
      name: 'Coder Agent',
      description: 'Writes and reviews code',
      type: 'Coder',
      status: 'inactive' as const,
    },
  ]

  return (
    <div className="space-y-8 p-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-slate-100">Dashboard</h1>
          <p className="mt-2 text-slate-400">Welcome back! Here's your AI agents overview.</p>
        </div>
        <Button variant="primary" size="lg">
          Create Agent
        </Button>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => {
          const Icon = stat.icon
          return (
            <Card key={stat.label} gradient>
              <CardContent className="pt-6">
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-sm text-slate-400">{stat.label}</p>
                    <p className="mt-2 text-3xl font-bold text-slate-100">{stat.value}</p>
                  </div>
                  <div className={`rounded-lg bg-gradient-to-br ${stat.color} p-3`}>
                    <Icon className="h-6 w-6 text-white" />
                  </div>
                </div>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 gap-8 lg:grid-cols-3">
        {/* Recent Agents */}
        <div className="lg:col-span-2">
          <div className="mb-6 flex items-center justify-between">
            <h2 className="text-2xl font-bold text-slate-100">Recent Agents</h2>
            <Button variant="outline" size="sm">
              View All
            </Button>
          </div>
          <div className="space-y-4">
            {recentAgents.map((agent) => (
              <AgentCard
                key={agent.id}
                {...agent}
                onEdit={() => console.log('Edit', agent.id)}
                onDelete={() => console.log('Delete', agent.id)}
                onDuplicate={() => console.log('Duplicate', agent.id)}
              />
            ))}
          </div>
        </div>

        {/* Quick Actions */}
        <div>
          <h2 className="mb-6 text-2xl font-bold text-slate-100">Quick Actions</h2>
          <Card>
            <CardContent className="space-y-3 pt-6">
              <Button variant="primary" size="md" className="w-full">
                Create Agent
              </Button>
              <Button variant="secondary" size="md" className="w-full">
                Create Workflow
              </Button>
              <Button variant="outline" size="md" className="w-full">
                View Executions
              </Button>
              <Button variant="ghost" size="md" className="w-full">
                Documentation
              </Button>
            </CardContent>
          </Card>

          {/* Stats Card */}
          <Card className="mt-6">
            <CardHeader>
              <CardTitle className="text-lg">System Status</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm text-slate-400">API Status</span>
                <span className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-green-500" />
                  <span className="text-sm text-green-400">Online</span>
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-slate-400">Database</span>
                <span className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-green-500" />
                  <span className="text-sm text-green-400">Connected</span>
                </span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-sm text-slate-400">Cache</span>
                <span className="flex items-center gap-2">
                  <div className="h-2 w-2 rounded-full bg-green-500" />
                  <span className="text-sm text-green-400">Active</span>
                </span>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
