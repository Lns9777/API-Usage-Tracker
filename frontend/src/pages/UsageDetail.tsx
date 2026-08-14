import { useParams } from 'react-router-dom'
import { PageState } from '../components/ui/PageState'
import { useUsage } from '../hooks/useUsage'

export default function UsageDetail() {
  const { id } = useParams()
  const { data, isLoading, isError } = useUsage()

  if (isLoading) {
    return <PageState title="Request Details" description="Loading request details..." />
  }

  if (isError || !data) {
    return <PageState title="Request Details" description="Unable to load request details." />
  }

  const record = data.find((row) => String(row.id) === id)

  if (!record) {
    return <PageState title="Request Details" description="Request not found." />
  }

  return (
    <div style={{ display: 'grid', gap: 24 }}>
      <div className="page">
        <h1>Request Details</h1>
        <p>{record.internal_request_id}</p>
      </div>
      <div className="page" style={{ display: 'grid', gap: 10 }}>
        <div>Project ID: {record.project_id}</div>
        <div>Provider ID: {record.provider_id}</div>
        <div>Model ID: {record.model_id}</div>
        <div>Timestamp: {new Date(record.timestamp).toLocaleString()}</div>
        <div>Latency: {Math.round(record.latency_ms)} ms</div>
        <div>Status: {record.status}</div>
        <div>HTTP Status: {record.http_status_code ?? '-'}</div>
        <div>Input Tokens: {record.input_tokens}</div>
        <div>Output Tokens: {record.output_tokens}</div>
        <div>Thinking Tokens: {record.thinking_tokens}</div>
        <div>Cached Tokens: {record.cached_tokens}</div>
        <div>Total Tokens: {record.total_tokens}</div>
        <div>Input Cost: ${record.input_cost.toFixed(4)}</div>
        <div>Output Cost: ${record.output_cost.toFixed(4)}</div>
        <div>Thinking Cost: ${record.thinking_cost.toFixed(4)}</div>
        <div>Cached Cost: ${record.cached_cost.toFixed(4)}</div>
        <div>Total Cost: ${record.total_cost.toFixed(4)}</div>
        <div>Content Capture: {record.capture_content ? 'Enabled' : 'Disabled'}</div>
      </div>
    </div>
  )
}
