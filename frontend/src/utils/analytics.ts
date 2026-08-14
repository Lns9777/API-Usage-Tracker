import type { UsageRecord } from '../types/usage'

export function countByStatus(records: UsageRecord[]) {
  return records.reduce<Record<string, number>>((acc, row) => {
    acc[row.status] = (acc[row.status] || 0) + 1
    return acc
  }, {})
}

export function maxCount(values: Record<string, number>) {
  return Math.max(...Object.values(values), 1)
}
