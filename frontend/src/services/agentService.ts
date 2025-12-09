import { apiClient } from './api'

export interface Agent {
  id: string
  name: string
  description: string
  type: string
  status: 'active' | 'inactive' | 'error'
  config?: Record<string, unknown>
  createdAt?: string
  updatedAt?: string
}

export interface CreateAgentRequest {
  name: string
  description: string
  type: string
  config?: Record<string, unknown>
}

export interface UpdateAgentRequest {
  name?: string
  description?: string
  type?: string
  config?: Record<string, unknown>
}

class AgentService {
  async listAgents(): Promise<Agent[]> {
    return apiClient.get<Agent[]>('/agents')
  }

  async getAgent(id: string): Promise<Agent> {
    return apiClient.get<Agent>(`/agents/${id}`)
  }

  async createAgent(data: CreateAgentRequest): Promise<Agent> {
    return apiClient.post<Agent>('/agents', data)
  }

  async updateAgent(id: string, data: UpdateAgentRequest): Promise<Agent> {
    return apiClient.put<Agent>(`/agents/${id}`, data)
  }

  async deleteAgent(id: string): Promise<void> {
    return apiClient.delete(`/agents/${id}`)
  }

  async duplicateAgent(id: string): Promise<Agent> {
    return apiClient.post<Agent>(`/agents/${id}/duplicate`)
  }
}

export const agentService = new AgentService()
