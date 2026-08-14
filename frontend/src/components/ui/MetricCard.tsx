type MetricCardProps = {
  label: string
  value: string
  delta?: string
}

export function MetricCard({ label, value, delta }: MetricCardProps) {
  return (
    <div style={{ border: '1px solid rgba(148,163,184,.18)', borderRadius: 16, padding: 18, background: 'rgba(15,23,42,.72)' }}>
      <div style={{ color: '#8aa0c7', fontSize: 13 }}>{label}</div>
      <div style={{ fontSize: 28, fontWeight: 700, marginTop: 6 }}>{value}</div>
      {delta ? <div style={{ color: '#60a5fa', marginTop: 6, fontSize: 12 }}>{delta}</div> : null}
    </div>
  )
}
