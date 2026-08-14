import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import { DataTable } from '../components/ui/DataTable'
import { MetricCard } from '../components/ui/MetricCard'
import { PageState } from '../components/ui/PageState'
import { useUsage } from '../hooks/useUsage'
import { DatePreset, filterUsage, summarizeUsage } from '../utils/usage'
import type { UsageRecord } from '../types/usage'

export default function Usage() {
  const { data, isLoading, isError } = useUsage()
  const [query, setQuery] = useState('')
  const [status, setStatus] = useState('all')
  const [range, setRange] = useState<DatePreset>('all')
  const [selected, setSelected] = useState<UsageRecord | null>(null)
  const filtered = useMemo(() => filterUsage(data ?? [], query, status, range), [data, query, status, range])
  const summary = useMemo(() => summarizeUsage(data ?? []), [data])

  if (isLoading) {
    return <PageState title="Usage" description="Loading API usage..." />
  }

  if (isError || !data) {
    return <PageState title="Usage" description="Unable to load usage records." />
  }

  return (
    <div style={{ display: 'grid', gap: 24 }}>
      <div className="page">
        <h1>Usage</h1>
        <p>Recent tracked requests.</p>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, minmax(0, 1fr))', gap: 16 }}>
        <MetricCard label="Requests" value={String(summary.requests)} />
        <MetricCard label="Input Tokens" value={summary.inputTokens.toLocaleString()} />
        <MetricCard label="Output Tokens" value={summary.outputTokens.toLocaleString()} />
        <MetricCard label="Total Tokens" value={summary.tokens.toLocaleString()} />
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, minmax(0, 1fr))', gap: 16 }}>
        <MetricCard label="Thinking Tokens" value={summary.thinkingTokens.toLocaleString()} />
        <MetricCard label="Cached Tokens" value={summary.cachedTokens.toLocaleString()} />
        <MetricCard label="Cost" value={`$${summary.cost.toFixed(4)}`} />
        <MetricCard label="Errors" value={String(summary.errors)} />
      </div>
      <div className="page" style={{ display: 'grid', gap: 12 }}>
        <h2>Filters</h2>
        <div style={{ display: 'grid', gap: 12, gridTemplateColumns: '2fr 1fr 1fr' }}>
          <input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search request id, project id, provider id, model id"
            style={{ background: '#0f172a', color: '#e5eefb', border: '1px solid rgba(148,163,184,.18)', borderRadius: 10, padding: 12 }}
          />
          <select
            value={status}
            onChange={(event) => setStatus(event.target.value)}
            style={{ background: '#0f172a', color: '#e5eefb', border: '1px solid rgba(148,163,184,.18)', borderRadius: 10, padding: 12 }}
          >
            <option value="all">All statuses</option>
            <option value="success">Success</option>
            <option value="error">Error</option>
          </select>
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
        </div>
      </div>
      <DataTable
        data={filtered}
        columns={[
          { header: 'Timestamp', cell: (row) => new Date(row.timestamp).toLocaleString() },
          { header: 'Project', cell: (row) => String(row.project_id) },
          { header: 'Provider', cell: (row) => String(row.provider_id) },
          { header: 'Model', cell: (row) => String(row.model_id) },
          { header: 'Request ID', cell: (row) => <button onClick={() => setSelected(row)} style={{ background: 'none', color: '#93c5fd', border: 0, padding: 0, cursor: 'pointer' }}>{row.internal_request_id}</button> },
          { header: 'Tokens', cell: (row) => row.total_tokens.toLocaleString() },
          { header: 'Cost', cell: (row) => `$${row.total_cost.toFixed(4)}` },
          { header: 'Latency', cell: (row) => `${Math.round(row.latency_ms)} ms` },
          { header: 'Status', cell: (row) => row.status },
        ]}
      />
      {selected ? (
        <div
          onClick={() => setSelected(null)}
          style={{ position: 'fixed', inset: 0, background: 'rgba(2,6,23,.72)', backdropFilter: 'blur(6px)', display: 'grid', placeItems: 'center', padding: 24, zIndex: 50 }}
        >
          <div
            onClick={(event) => event.stopPropagation()}
            style={{ width: 'min(820px, 100%)', maxHeight: '90vh', overflow: 'auto', background: 'linear-gradient(180deg, #0f172a, #111827)', border: '1px solid rgba(148,163,184,.2)', borderRadius: 18, padding: 24, display: 'grid', gap: 14, boxShadow: '0 24px 80px rgba(0,0,0,.45)' }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', gap: 16 }}>
              <div>
                <h2 style={{ margin: 0 }}>Request Details</h2>
                <p style={{ margin: '6px 0 0', color: '#8aa0c7' }}>{selected.internal_request_id}</p>
              </div>
              <button onClick={() => setSelected(null)} style={{ background: '#1f2937', color: '#e5eefb', border: 0, borderRadius: 10, padding: '8px 12px' }}>
                Close
              </button>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, minmax(0, 1fr))', gap: 12 }}>
              <div style={{ background: 'rgba(15,23,42,.7)', border: '1px solid rgba(148,163,184,.12)', borderRadius: 12, padding: 12 }}>Project ID: {selected.project_id}</div>
              <div style={{ background: 'rgba(15,23,42,.7)', border: '1px solid rgba(148,163,184,.12)', borderRadius: 12, padding: 12 }}>Provider ID: {selected.provider_id}</div>
              <div style={{ background: 'rgba(15,23,42,.7)', border: '1px solid rgba(148,163,184,.12)', borderRadius: 12, padding: 12 }}>Model ID: {selected.model_id}</div>
              <div style={{ background: 'rgba(15,23,42,.7)', border: '1px solid rgba(148,163,184,.12)', borderRadius: 12, padding: 12 }}>Timestamp: {new Date(selected.timestamp).toLocaleString()}</div>
              <div style={{ background: 'rgba(15,23,42,.7)', border: '1px solid rgba(148,163,184,.12)', borderRadius: 12, padding: 12 }}>Latency: {Math.round(selected.latency_ms)} ms</div>
              <div style={{ background: 'rgba(15,23,42,.7)', border: '1px solid rgba(148,163,184,.12)', borderRadius: 12, padding: 12 }}>Status: {selected.status}</div>
              <div style={{ background: 'rgba(15,23,42,.7)', border: '1px solid rgba(148,163,184,.12)', borderRadius: 12, padding: 12 }}>HTTP Status: {selected.http_status_code ?? '-'}</div>
              <div style={{ background: 'rgba(15,23,42,.7)', border: '1px solid rgba(148,163,184,.12)', borderRadius: 12, padding: 12 }}>Capture Content: {selected.capture_content ? 'Enabled' : 'Disabled'}</div>
              <div style={{ background: 'rgba(15,23,42,.7)', border: '1px solid rgba(148,163,184,.12)', borderRadius: 12, padding: 12 }}>Input Tokens: {selected.input_tokens}</div>
              <div style={{ background: 'rgba(15,23,42,.7)', border: '1px solid rgba(148,163,184,.12)', borderRadius: 12, padding: 12 }}>Output Tokens: {selected.output_tokens}</div>
              <div style={{ background: 'rgba(15,23,42,.7)', border: '1px solid rgba(148,163,184,.12)', borderRadius: 12, padding: 12 }}>Thinking Tokens: {selected.thinking_tokens}</div>
              <div style={{ background: 'rgba(15,23,42,.7)', border: '1px solid rgba(148,163,184,.12)', borderRadius: 12, padding: 12 }}>Cached Tokens: {selected.cached_tokens}</div>
              <div style={{ background: 'rgba(15,23,42,.7)', border: '1px solid rgba(148,163,184,.12)', borderRadius: 12, padding: 12 }}>Total Tokens: {selected.total_tokens}</div>
              <div style={{ background: 'rgba(15,23,42,.7)', border: '1px solid rgba(148,163,184,.12)', borderRadius: 12, padding: 12 }}>Input Cost: ${selected.input_cost.toFixed(4)}</div>
              <div style={{ background: 'rgba(15,23,42,.7)', border: '1px solid rgba(148,163,184,.12)', borderRadius: 12, padding: 12 }}>Output Cost: ${selected.output_cost.toFixed(4)}</div>
              <div style={{ background: 'rgba(15,23,42,.7)', border: '1px solid rgba(148,163,184,.12)', borderRadius: 12, padding: 12 }}>Thinking Cost: ${selected.thinking_cost.toFixed(4)}</div>
              <div style={{ background: 'rgba(15,23,42,.7)', border: '1px solid rgba(148,163,184,.12)', borderRadius: 12, padding: 12 }}>Cached Cost: ${selected.cached_cost.toFixed(4)}</div>
              <div style={{ background: 'rgba(15,23,42,.7)', border: '1px solid rgba(148,163,184,.12)', borderRadius: 12, padding: 12 }}>Total Cost: ${selected.total_cost.toFixed(4)}</div>
            </div>
            {selected.error_type ? <div>Error Type: {selected.error_type}</div> : null}
            <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
              <Link to={`/usage/${selected.id}`}>Open dedicated view</Link>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  )
}
