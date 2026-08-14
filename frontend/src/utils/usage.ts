import type { UsageRecord } from '../types/usage'

export type DatePreset = 'all' | 'today' | 'yesterday' | '7d' | '30d'

export function getDateBoundary(preset: DatePreset) {
  const now = new Date()
  const start = new Date(now)
  start.setHours(0, 0, 0, 0)

  if (preset === 'today') return start
  if (preset === 'yesterday') {
    start.setDate(start.getDate() - 1)
    return start
  }
  if (preset === '7d') {
    start.setDate(start.getDate() - 6)
    return start
  }
  if (preset === '30d') {
    start.setDate(start.getDate() - 29)
    return start
  }
  return null
}

export function filterUsage(records: UsageRecord[], query: string, status: string, range: DatePreset = 'all'): UsageRecord[] {
  const q = query.trim().toLowerCase()
  const boundary = getDateBoundary(range)
  return records.filter((row) => {
    const rowDate = new Date(row.timestamp)
    const matchesDate = !boundary || rowDate >= boundary
    const matchesQuery =
      !q ||
      row.internal_request_id.toLowerCase().includes(q) ||
      String(row.project_id).includes(q) ||
      String(row.provider_id).includes(q) ||
      String(row.model_id).includes(q)
    const matchesStatus = status === 'all' || row.status === status
    return matchesDate && matchesQuery && matchesStatus
  })
}

export function summarizeUsage(records: UsageRecord[]) {
  return {
    requests: records.length,
    inputTokens: records.reduce((sum, row) => sum + row.input_tokens, 0),
    outputTokens: records.reduce((sum, row) => sum + row.output_tokens, 0),
    thinkingTokens: records.reduce((sum, row) => sum + row.thinking_tokens, 0),
    cachedTokens: records.reduce((sum, row) => sum + row.cached_tokens, 0),
    tokens: records.reduce((sum, row) => sum + row.total_tokens, 0),
    cost: records.reduce((sum, row) => sum + row.total_cost, 0),
    errors: records.filter((row) => row.status !== 'success').length,
  }
}
