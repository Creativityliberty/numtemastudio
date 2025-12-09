import { Workflow, workflowService } from '@/services/workflowService'
import { create } from 'zustand'

interface WorkflowState {
  workflows: Workflow[]
  selectedWorkflow: Workflow | null
  isLoading: boolean
  error: string | null
  
  // Actions
  fetchWorkflows: () => Promise<void>
  getWorkflow: (id: string) => Promise<void>
  selectWorkflow: (workflow: Workflow | null) => void
  createWorkflow: (data: any) => Promise<void>
  updateWorkflow: (id: string, data: any) => Promise<void>
  deleteWorkflow: (id: string) => Promise<void>
  executeWorkflow: (id: string, input?: any) => Promise<void>
  clearError: () => void
}

export const useWorkflowStore = create<WorkflowState>((set) => ({
  workflows: [],
  selectedWorkflow: null,
  isLoading: false,
  error: null,

  fetchWorkflows: async () => {
    set({ isLoading: true, error: null })
    try {
      const workflows = await workflowService.listWorkflows()
      set({ workflows, isLoading: false })
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false })
    }
  },

  getWorkflow: async (id: string) => {
    set({ isLoading: true, error: null })
    try {
      const workflow = await workflowService.getWorkflow(id)
      set({ selectedWorkflow: workflow, isLoading: false })
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false })
    }
  },

  selectWorkflow: (workflow: Workflow | null) => {
    set({ selectedWorkflow: workflow })
  },

  createWorkflow: async (data: any) => {
    set({ isLoading: true, error: null })
    try {
      const newWorkflow = await workflowService.createWorkflow(data)
      set((state) => ({
        workflows: [...state.workflows, newWorkflow],
        isLoading: false,
      }))
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false })
    }
  },

  updateWorkflow: async (id: string, data: any) => {
    set({ isLoading: true, error: null })
    try {
      const updatedWorkflow = await workflowService.updateWorkflow(id, data)
      set((state) => ({
        workflows: state.workflows.map((w) => (w.id === id ? updatedWorkflow : w)),
        selectedWorkflow: state.selectedWorkflow?.id === id ? updatedWorkflow : state.selectedWorkflow,
        isLoading: false,
      }))
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false })
    }
  },

  deleteWorkflow: async (id: string) => {
    set({ isLoading: true, error: null })
    try {
      await workflowService.deleteWorkflow(id)
      set((state) => ({
        workflows: state.workflows.filter((w) => w.id !== id),
        selectedWorkflow: state.selectedWorkflow?.id === id ? null : state.selectedWorkflow,
        isLoading: false,
      }))
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false })
    }
  },

  executeWorkflow: async (id: string, input?: any) => {
    set({ isLoading: true, error: null })
    try {
      await workflowService.executeWorkflow(id, input)
      set({ isLoading: false })
    } catch (error) {
      set({ error: (error as Error).message, isLoading: false })
    }
  },

  clearError: () => {
    set({ error: null })
  },
}))
