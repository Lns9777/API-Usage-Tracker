import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { Navigate, Route, Routes } from 'react-router-dom'
import DashboardLayout from './layouts/DashboardLayout'
import Dashboard from './pages/Dashboard'
import Projects from './pages/Projects'
import Usage from './pages/Usage'
import Analytics from './pages/Analytics'
import Providers from './pages/Providers'
import Models from './pages/Models'
import Pricing from './pages/Pricing'
import ProjectDetails from './pages/ProjectDetails'
import UsageDetail from './pages/UsageDetail'
import Errors from './pages/Errors'
import Settings from './pages/Settings'

const queryClient = new QueryClient()

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Routes>
        <Route element={<DashboardLayout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/projects" element={<Projects />} />
          <Route path="/usage" element={<Usage />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/providers" element={<Providers />} />
          <Route path="/models" element={<Models />} />
          <Route path="/pricing" element={<Pricing />} />
          <Route path="/usage/:id" element={<UsageDetail />} />
          <Route path="/projects/:id" element={<ProjectDetails />} />
          <Route path="/errors" element={<Errors />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </QueryClientProvider>
  )
}
