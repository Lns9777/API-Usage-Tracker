import { describe, expect, it } from 'vitest'
import { countByStatus, maxCount } from './analytics'

const records = [
  { status: 'success' },
  { status: 'success' },
  { status: 'error' },
] as const

describe('analytics helpers', () => {
  it('counts records by status', () => {
    expect(countByStatus(records as never)).toEqual({
      success: 2,
      error: 1,
    })
  })

  it('computes a safe max count', () => {
    expect(maxCount({ success: 2, error: 1 })).toBe(2)
    expect(maxCount({})).toBe(1)
  })
})
