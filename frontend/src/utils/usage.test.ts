import { describe, expect, it, vi } from 'vitest'
import { filterUsage, getDateBoundary, summarizeUsage } from './usage'

const records = [
  {
    id: 1,
    project_id: 10,
    provider_id: 20,
    model_id: 30,
    internal_request_id: 'req-alpha',
    timestamp: '2026-08-13T00:00:00Z',
    input_tokens: 1,
    output_tokens: 2,
    thinking_tokens: 0,
    cached_tokens: 0,
    total_tokens: 3,
    input_cost: 0.1,
    output_cost: 0.2,
    thinking_cost: 0,
    cached_cost: 0,
    total_cost: 0.3,
    latency_ms: 100,
    status: 'success',
  },
  {
    id: 2,
    project_id: 11,
    provider_id: 21,
    model_id: 31,
    internal_request_id: 'req-beta',
    timestamp: '2026-08-13T00:00:00Z',
    input_tokens: 4,
    output_tokens: 5,
    thinking_tokens: 0,
    cached_tokens: 0,
    total_tokens: 9,
    input_cost: 0.4,
    output_cost: 0.5,
    thinking_cost: 0,
    cached_cost: 0,
    total_cost: 0.9,
    latency_ms: 200,
    status: 'error',
  },
] as const

describe('usage helpers', () => {
  it('filters by query and status', () => {
    expect(filterUsage(records as never, 'alpha', 'all')).toHaveLength(1)
    expect(filterUsage(records as never, '11', 'all')).toHaveLength(1)
    expect(filterUsage(records as never, '', 'error')).toHaveLength(1)
  })

  it('filters by date preset', () => {
    vi.useFakeTimers()
    vi.setSystemTime(new Date('2026-08-13T12:00:00Z'))
    expect(getDateBoundary('today')?.toISOString()).toContain('2026-08-12')
    expect(getDateBoundary('yesterday')?.toISOString()).toContain('2026-08-11')
    vi.useRealTimers()
  })

  it('summarizes usage', () => {
    expect(summarizeUsage(records as never)).toEqual({
      requests: 2,
      inputTokens: 5,
      outputTokens: 7,
      thinkingTokens: 0,
      cachedTokens: 0,
      tokens: 12,
      cost: 1.2,
      errors: 1,
    })
  })
})
