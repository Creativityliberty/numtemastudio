import { apiClient } from './api'

export interface WorkflowNode {
  id: string
  type: 'agent' | 'data' | 'logic' | 'action'
  label: string
  config?: Record<string, unknown>
}

export interface WorkflowEdge {
  source: string
  target: string
  label?: string
}

export interface Workflow {
  id: string
  name: string
  description: string
  nodes: WorkflowNode[]
  edges: WorkflowEdge[]
  status: 'active' | 'inactive'
  createdAt?: string
  updatedAt?: string
}

export interface CreateWorkflowRequest {
  name: string
  description: string
  nodes: WorkflowNode[]
  edges: WorkflowEdge[]
}

export interface UpdateWorkflowRequest {
  name?: string
  description?: string
  nodes?: WorkflowNode[]
  edges?: WorkflowEdge[]
  status?: 'active' | 'inactive'
}

class WorkflowService {
  async listWorkflows(): Promise<Workflow[]> {
    return apiClient.get<Workflow[]>('/workflows')
  }

  async getWorkflow(id: string): Promise<Workflow> {
    return apiClient.get<Workflow>(`/workflows/${id}`)
  }

  async createWorkflow(data: CreateWorkflowRequest): Promise<Workflow> {
    return apiClient.post<Workflow>('/workflows', data)
  }

  async updateWorkflow(id: string, data: UpdateWorkflowRequest): Promise<Workflow> {
    return apiClient.put<Workflow>(`/workflows/${id}`, data)
  }

  async deleteWorkflow(id: string): Promise<void> {
    return apiClient.delete(`/workflows/${id}`)
  }

  async executeWorkflow(id: string, input?: Record<string, unknown>): Promise<unknown> {
    return apiClient.post(`/workflows/${id}/execute`, { input })
  }
}

export const workflowService = new WorkflowService()
