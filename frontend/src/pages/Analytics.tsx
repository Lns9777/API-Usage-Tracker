import { DataTable } from '../components/ui/DataTable'
import { MetricCard } from '../components/ui/MetricCard'
import { PageState } from '../components/ui/PageState'
import { MiniBarChart } from '../components/charts/MiniBarChart'
import { useAnalytics } from '../hooks/useAnalytics'
import { useUsage } from '../hooks/useUsage'
import { countByStatus, maxCount } from '../utils/analytics'

export default function Analytics() {
  const overview = useAnalytics()
  const usage = useUsage()

  if (overview.isLoading || usage.isLoading) {
    return <PageState title="Analytics" description="Loading analytics..." />
  }

  if (overview.isError || usage.isError || !overview.data || !usage.data) {
    return <PageState title="Analytics" description="Unable to load analytics." />
  }

  const byStatus = countByStatus(usage.data)
  const maxStatus = maxCount(byStatus)

  return (
    <div style={{ display: 'grid', gap: 24 }}>
      <div className="page">
        <h1>Analytics</h1>
        <p>Cost, usage, and reliability snapshots.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, minmax(0, 1fr))', gap: 16 }}>
        <MetricCard label="Requests" value={String(overview.data.requests)} />
        <MetricCard label="Tokens" value={overview.data.tokens.toLocaleString()} />
        <MetricCard label="Cost" value={`$${overview.data.cost.toFixed(4)}`} />
        <MetricCard label="Error Rate" value={`${overview.data.error_rate.toFixed(2)}%`} />
      </div>

      <div className="page">
        <h2>Request Status</h2>
        <div style={{ display: 'grid', gap: 14, marginTop: 16 }}>
          {Object.entries(byStatus).map(([status, count]) => (
            <MiniBarChart key={status} label={status} value={count} max={maxStatus} />
          ))}
        </div>
      </div>

      <DataTable
        data={Object.entries(byStatus).map(([status, count]) => ({ status, count }))}
        columns={[
          { header: 'Status', cell: (row: { status: string; count: number }) => row.status },
          { header: 'Count', cell: (row: { status: string; count: number }) => String(row.count) },
        ]}
        emptyMessage="No usage yet."
      />
    </div>
  )
}
