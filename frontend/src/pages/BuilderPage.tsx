import Button from '@/components/common/Button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/common/Card'
import Input from '@/components/common/Input'
import Modal from '@/components/common/Modal'
import { MessageCircle, Send, Zap } from 'lucide-react'
import React, { useState } from 'react'

const BuilderPage: React.FC = () => {
  const [messages, setMessages] = useState<Array<{ role: 'user' | 'assistant'; content: string }>>([
    { role: 'assistant', content: 'Hello! I\'m the Agent Builder. I can help you create and manage AI agents. What would you like to do?' }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [showHistory, setShowHistory] = useState(false)

  const handleSend = async () => {
    if (!input.trim()) return

    setMessages((prev) => [...prev, { role: 'user', content: input }])
    setInput('')
    setIsLoading(true)

    // Simulate API call
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: `I'll help you with: "${input}". This is a simulated response. In production, this would be connected to the backend Agent Builder.`
        }
      ])
      setIsLoading(false)
    }, 1000)
  }

  return (
    <div className="flex h-screen flex-col gap-8 p-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold text-slate-100">Agent Builder</h1>
          <p className="mt-2 text-slate-400">Chat with AI to create and manage agents</p>
        </div>
        <Button
          variant="outline"
          size="lg"
          icon={<MessageCircle size={20} />}
          onClick={() => setShowHistory(true)}
        >
          History
        </Button>
      </div>

      {/* Chat Area */}
      <div className="flex flex-1 gap-6 overflow-hidden">
        {/* Main Chat */}
        <div className="flex flex-1 flex-col gap-4">
          {/* Messages */}
          <Card className="flex-1 overflow-hidden">
            <CardContent className="flex h-full flex-col overflow-y-auto pt-6">
              <div className="space-y-4">
                {messages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-xs rounded-lg px-4 py-2 ${
                        msg.role === 'user'
                          ? 'bg-indigo-600 text-white'
                          : 'bg-slate-700 text-slate-100'
                      }`}
                    >
                      {msg.content}
                    </div>
                  </div>
                ))}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="rounded-lg bg-slate-700 px-4 py-2 text-slate-100">
                      <div className="flex gap-2">
                        <div className="h-2 w-2 animate-bounce rounded-full bg-slate-400" />
                        <div className="h-2 w-2 animate-bounce rounded-full bg-slate-400" style={{ animationDelay: '0.1s' }} />
                        <div className="h-2 w-2 animate-bounce rounded-full bg-slate-400" style={{ animationDelay: '0.2s' }} />
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>

          {/* Input */}
          <Card>
            <CardContent className="flex gap-3 pt-6">
              <Input
                placeholder="Describe what you want to create..."
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault()
                    handleSend()
                  }
                }}
                disabled={isLoading}
              />
              <Button
                variant="primary"
                size="md"
                icon={<Send size={20} />}
                onClick={handleSend}
                isLoading={isLoading}
              >
                Send
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Sidebar */}
        <div className="hidden w-80 flex-col gap-4 lg:flex">
          {/* Quick Actions */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <Button variant="secondary" size="md" className="w-full" icon={<Zap size={18} />}>
                Create Agent
              </Button>
              <Button variant="secondary" size="md" className="w-full">
                Create Workflow
              </Button>
              <Button variant="outline" size="md" className="w-full">
                View Agents
              </Button>
            </CardContent>
          </Card>

          {/* Recent Actions */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Recent Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="rounded-lg bg-slate-700/50 p-3">
                <p className="text-sm font-medium text-slate-100">Created Research Agent</p>
                <p className="text-xs text-slate-400">2 hours ago</p>
              </div>
              <div className="rounded-lg bg-slate-700/50 p-3">
                <p className="text-sm font-medium text-slate-100">Updated Writer Workflow</p>
                <p className="text-xs text-slate-400">5 hours ago</p>
              </div>
              <div className="rounded-lg bg-slate-700/50 p-3">
                <p className="text-sm font-medium text-slate-100">Deleted Test Agent</p>
                <p className="text-xs text-slate-400">1 day ago</p>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* History Modal */}
      <Modal
        isOpen={showHistory}
        onClose={() => setShowHistory(false)}
        title="Builder History"
        size="lg"
      >
        <div className="space-y-3">
          <div className="rounded-lg bg-slate-700/50 p-4">
            <p className="text-sm font-medium text-slate-100">Create a research agent</p>
            <p className="mt-1 text-xs text-slate-400">Created agent: Research Agent</p>
          </div>
          <div className="rounded-lg bg-slate-700/50 p-4">
            <p className="text-sm font-medium text-slate-100">Build a workflow</p>
            <p className="mt-1 text-xs text-slate-400">Created workflow: Research & Write</p>
          </div>
        </div>
      </Modal>
    </div>
  )
}

export default BuilderPage
