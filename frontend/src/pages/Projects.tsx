import { DataTable } from '../components/ui/DataTable'
import { MetricCard } from '../components/ui/MetricCard'
import { PageState } from '../components/ui/PageState'
import { useProjects } from '../hooks/useProjects'

export default function Projects() {
  const { data, isLoading, isError } = useProjects()

  if (isLoading) {
    return <PageState title="Projects" description="Loading projects..." />
  }

  if (isError || !data) {
    return <PageState title="Projects" description="Unable to load projects." />
  }

  return (
    <div style={{ display: 'grid', gap: 24 }}>
      <div className="page">
        <h1>Projects</h1>
        <p>Project-level usage and cost breakdown.</p>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, minmax(0, 1fr))', gap: 16 }}>
        <MetricCard label="Projects" value={String(data.length)} />
        <MetricCard label="Production" value={String(data.filter((row) => row.environment === 'production').length)} />
        <MetricCard label="Development" value={String(data.filter((row) => row.environment !== 'production').length)} />
      </div>
      <DataTable
        data={data}
        columns={[
          { header: 'Name', cell: (row) => row.name },
          { header: 'Environment', cell: (row) => row.environment },
          { header: 'Description', cell: (row) => row.description || '-' },
          { header: 'Created', cell: (row) => new Date(row.created_at).toLocaleString() },
        ]}
      />
    </div>
  )
}
