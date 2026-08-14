type MiniBarChartProps = {
  label: string
  value: number
  max: number
}

export function MiniBarChart({ label, value, max }: MiniBarChartProps) {
  const width = max > 0 ? Math.max((value / max) * 100, 4) : 4

  return (
    <div style={{ display: 'grid', gap: 8 }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', color: '#c7d2fe', fontSize: 13 }}>
        <span>{label}</span>
        <span>{value.toLocaleString()}</span>
      </div>
      <div style={{ height: 10, borderRadius: 999, background: 'rgba(148,163,184,.14)', overflow: 'hidden' }}>
        <div style={{ width: `${width}%`, height: '100%', background: 'linear-gradient(90deg, #60a5fa, #34d399)' }} />
      </div>
    </div>
  )
}
