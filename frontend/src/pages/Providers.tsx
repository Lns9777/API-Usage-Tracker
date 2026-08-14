import { useState, type FormEvent } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { DataTable } from '../components/ui/DataTable'
import { MetricCard } from '../components/ui/MetricCard'
import { PageState } from '../components/ui/PageState'
import { useProviders } from '../hooks/useProviders'
import { createProvider } from '../services/providers'

export default function Providers() {
  const queryClient = useQueryClient()
  const { data, isLoading, isError } = useProviders()
  const [name, setName] = useState('')
  const [message, setMessage] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const createMutation = useMutation({
    mutationFn: createProvider,
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['providers'] })
      setName('')
      setMessage('Provider added successfully.')
      setError(null)
    },
    onError: () => {
      setMessage(null)
      setError('Unable to add provider. Please try again.')
    },
  })

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setMessage(null)
    setError(null)

    if (!name.trim()) {
      setError('Provider name is required.')
      return
    }

    createMutation.mutate(name.trim())
  }

  if (isLoading) {
    return <PageState title="Providers" description="Loading providers..." />
  }

  if (isError || !data) {
    return <PageState title="Providers" description="Unable to load providers." />
  }

  return (
    <div style={{ display: 'grid', gap: 24 }}>
      <div className="page">
        <h1>Providers</h1>
        <p>Registered API providers in the local tracker.</p>
      </div>
      <div
        style={{
          border: '1px solid rgba(148,163,184,.18)',
          borderRadius: 20,
          background: 'linear-gradient(180deg, rgba(15,23,42,.92), rgba(15,23,42,.76))',
          padding: 20,
          display: 'grid',
          gap: 16,
        }}
      >
        <div>
          <h2 style={{ margin: 0 }}>Add Provider</h2>
          <p style={{ margin: '6px 0 0', color: '#8aa0c7' }}>Create a local provider record for tracking usage and models.</p>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', gap: 12, flexWrap: 'wrap', alignItems: 'center' }}>
          <input
            value={name}
            onChange={(event) => setName(event.target.value)}
            placeholder="Provider name"
            style={{ minWidth: 280, padding: 12, borderRadius: 12, border: '1px solid rgba(148,163,184,.18)', background: '#0f172a', color: '#e2e8f0' }}
          />
          <button
            type="submit"
            disabled={createMutation.isPending}
            style={{
              padding: '12px 18px',
              borderRadius: 12,
              border: 'none',
              background: createMutation.isPending ? '#475569' : 'linear-gradient(135deg, #22c55e, #14b8a6)',
              color: '#fff',
              fontWeight: 700,
              cursor: createMutation.isPending ? 'wait' : 'pointer',
            }}
          >
            {createMutation.isPending ? 'Saving...' : 'Add Provider'}
          </button>
          {message ? <span style={{ color: '#86efac' }}>{message}</span> : null}
          {error ? <span style={{ color: '#fca5a5' }}>{error}</span> : null}
        </form>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, minmax(0, 1fr))', gap: 16 }}>
        <MetricCard label="Providers" value={String(data.length)} />
        <MetricCard label="Active Names" value={String(new Set(data.map((row) => row.name)).size)} />
        <MetricCard label="Newest ID" value={String(data[0]?.id ?? 0)} />
      </div>
      <DataTable
        data={data}
        columns={[
          { header: 'ID', cell: (row) => String(row.id) },
          { header: 'Name', cell: (row) => row.name },
          { header: 'Created', cell: (row) => new Date(row.created_at).toLocaleString() },
        ]}
      />
    </div>
  )
}
