import MainLayout from '@/components/layout/MainLayout'
import AgentsPage from '@/pages/AgentsPage'
import BuilderPage from '@/pages/BuilderPage'
import Dashboard from '@/pages/Dashboard'
import SettingsPage from '@/pages/SettingsPage'
import WorkflowsPage from '@/pages/WorkflowsPage'
import { Route, BrowserRouter as Router, Routes } from 'react-router-dom'

function App() {
  return (
    <Router>
      <Routes>
        <Route element={<MainLayout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/agents" element={<AgentsPage />} />
          <Route path="/workflows" element={<WorkflowsPage />} />
          <Route path="/builder" element={<BuilderPage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App
