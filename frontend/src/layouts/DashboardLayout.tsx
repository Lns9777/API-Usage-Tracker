import { NavLink, Outlet } from 'react-router-dom'

const items = ['/', '/projects', '/usage', '/analytics', '/providers', '/models', '/pricing', '/errors', '/settings']

export default function DashboardLayout() {
  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">API Tracker</div>
        {items.map((path) => (
          <NavLink key={path} to={path}>{path === '/' ? 'Overview' : path.slice(1).replace('-', ' ').replace(/\b\w/g, (s) => s.toUpperCase())}</NavLink>
        ))}
      </aside>
      <main className="content">
        <Outlet />
      </main>
    </div>
  )
}
