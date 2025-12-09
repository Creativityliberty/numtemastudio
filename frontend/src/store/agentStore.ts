import { Agent, agentService } from '@/services/agentService'
import { create } from 'zustand'

interface AgentState {
  agents: Agent[]
  selectedAgent: Agent | null
  isLoading: boolean
  error: string | null
  
  // Actions
  fetchAgents: () => Promise<void>
  getAgent: (id: string) => Promise<void>
  selectAgent: (agent: Agent | null) => void
  createAgent: (data: any) => Promise<void>
  updateAgent: (id: string, data: any) => Promise<void>
  deleteAgent: (id: string) => Promise<void>
  duplicateAgent: (id: string) => Promise<void>
  clearError: () => void
}

export const useAgentStore = create<AgentState>((set) => ({
  agents: [],
  selectedAgent: null,
  isLoading: false,
  error: null,

  fetchAgents: async () => {
    set({ isLoading: true, error: null })
    try {
      const agents = await agentService.listAgents()
      set({ agents, isLoading: false })
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false })
    }
  },

  getAgent: async (id: string) => {
    set({ isLoading: true, error: null })
    try {
      const agent = await agentService.getAgent(id)
      set({ selectedAgent: agent, isLoading: false })
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false })
    }
  },

  selectAgent: (agent: Agent | null) => {
    set({ selectedAgent: agent })
  },

  createAgent: async (data: any) => {
    set({ isLoading: true, error: null })
    try {
      const newAgent = await agentService.createAgent(data)
      set((state) => ({
        agents: [...state.agents, newAgent],
        isLoading: false,
      }))
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false })
    }
  },

  updateAgent: async (id: string, data: any) => {
    set({ isLoading: true, error: null })
    try {
      const updatedAgent = await agentService.updateAgent(id, data)
      set((state) => ({
        agents: state.agents.map((a) => (a.id === id ? updatedAgent : a)),
        selectedAgent: state.selectedAgent?.id === id ? updatedAgent : state.selectedAgent,
        isLoading: false,
      }))
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false })
    }
  },

  deleteAgent: async (id: string) => {
    set({ isLoading: true, error: null })
    try {
      await agentService.deleteAgent(id)
      set((state) => ({
        agents: state.agents.filter((a) => a.id !== id),
        selectedAgent: state.selectedAgent?.id === id ? null : state.selectedAgent,
        isLoading: false,
      }))
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false })
    }
  },

  duplicateAgent: async (id: string) => {
    set({ isLoading: true, error: null })
    try {
      const duplicatedAgent = await agentService.duplicateAgent(id)
      set((state) => ({
        agents: [...state.agents, duplicatedAgent],
        isLoading: false,
      }))
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false })
    }
  },

  clearError: () => {
    set({ error: null })
  },
}))
