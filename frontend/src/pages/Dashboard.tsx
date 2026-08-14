import { useMemo, useState } from 'react'
import { MetricCard } from '../components/ui/MetricCard'
import { PageState } from '../components/ui/PageState'
import { useAnalytics } from '../hooks/useAnalytics'
import { DatePreset, filterUsage, summarizeUsage } from '../utils/usage'
import { useUsage } from '../hooks/useUsage'

export default function Dashboard() {
  const { data, isLoading, isError } = useAnalytics()
  const usage = useUsage()
  const [range, setRange] = useState<DatePreset>('all')
  const filteredUsage = useMemo(() => filterUsage(usage.data ?? [], '', 'all', range), [usage.data, range])
  const summary = useMemo(() => summarizeUsage(filteredUsage), [filteredUsage])

  if (isLoading || usage.isLoading) {
    return <PageState title="Overview" description="Loading dashboard metrics..." />
  }

  if (isError || usage.isError || !data || !usage.data) {
    return <PageState title="Overview" description="Unable to load analytics." />
  }

  return (
    <div style={{ display: 'grid', gap: 24 }}>
      <div className="page">
        <h1>Overview</h1>
        <p>Real-time usage, cost, and reliability snapshot.</p>
      </div>
      <div className="page" style={{ display: 'grid', gap: 12 }}>
        <h2>Date Range</h2>
        <div style={{ display: 'grid', gap: 12, gridTemplateColumns: '1fr 1fr' }}>
          <select
            value={range}
            onChange={(event) => setRange(event.target.value as DatePreset)}
            style={{ background: '#0f172a', color: '#e5eefb', border: '1px solid rgba(148,163,184,.18)', borderRadius: 10, padding: 12 }}
          >
            <option value="all">All time</option>
            <option value="today">Today</option>
            <option value="yesterday">Yesterday</option>
            <option value="7d">Last 7 days</option>
            <option value="30d">Last 30 days</option>
          </select>
          <div style={{ color: '#8aa0c7', alignSelf: 'center' }}>Showing: {range === 'all' ? 'All time' : range}</div>
        </div>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, minmax(0, 1fr))', gap: 16 }}>
        <MetricCard label="Total Requests" value={String(summary.requests)} />
        <MetricCard label="Total Tokens" value={summary.tokens.toLocaleString()} />
        <MetricCard label="Total Cost" value={`$${data.cost.toFixed(4)}`} />
        <MetricCard label="Avg Latency" value={`${Math.round(data.average_latency_ms)} ms`} />
        <MetricCard label="Error Rate" value={`${data.error_rate.toFixed(2)}%`} />
      </div>
      <div className="page">
        <h2>What to watch</h2>
        <ul>
          <li>Track pricing changes through versioned records only.</li>
          <li>Use the usage table to inspect provider and model mix.</li>
          <li>Keep prompts, responses, and secrets off the local store.</li>
        </ul>
      </div>
    </div>
  )
}
