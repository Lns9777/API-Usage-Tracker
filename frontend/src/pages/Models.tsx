import { useMemo, useState, type FormEvent } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { DataTable } from '../components/ui/DataTable'
import { MetricCard } from '../components/ui/MetricCard'
import { PageState } from '../components/ui/PageState'
import { useProviders } from '../hooks/useProviders'
import { useModels } from '../hooks/useModels'
import { createModel } from '../services/models'

export default function Models() {
  const queryClient = useQueryClient()
  const { data, isLoading, isError } = useModels()
  const { data: providers = [] } = useProviders()
  const [providerId, setProviderId] = useState(0)
  const [modelName, setModelName] = useState('')
  const [modelType, setModelType] = useState('text')
  const [message, setMessage] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const providerOptions = useMemo(
    () => providers.map((provider) => ({ id: provider.id, label: `${provider.name} (#${provider.id})` })),
    [providers],
  )

  const createMutation = useMutation({
    mutationFn: createModel,
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['models'] })
      setProviderId(0)
      setModelName('')
      setModelType('text')
      setMessage('Model added successfully.')
      setError(null)
    },
    onError: () => {
      setMessage(null)
      setError('Unable to add model. Please check the form and try again.')
    },
  })

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setMessage(null)
    setError(null)

    if (!providerId) {
      setError('Provider is required.')
      return
    }

    if (!modelName.trim()) {
      setError('Model name is required.')
      return
    }

    createMutation.mutate({
      provider_id: providerId,
      model_name: modelName.trim(),
      model_type: modelType,
    })
  }

  if (isLoading) {
    return <PageState title="Models" description="Loading models..." />
  }

  if (isError || !data) {
    return <PageState title="Models" description="Unable to load models." />
  }

  return (
    <div style={{ display: 'grid', gap: 24 }}>
      <div className="page">
        <h1>Models</h1>
        <p>Model registry and provider mappings.</p>
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
          <h2 style={{ margin: 0 }}>Add Model</h2>
          <p style={{ margin: '6px 0 0', color: '#8aa0c7' }}>Create a new local model mapping for a provider.</p>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'grid', gap: 16 }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, minmax(0, 1fr))', gap: 16 }}>
            <label style={{ display: 'grid', gap: 8 }}>
              <span style={{ color: '#8aa0c7', fontSize: 13 }}>Provider</span>
              <select
                value={providerId}
                onChange={(event) => setProviderId(Number(event.target.value))}
                style={{ padding: 12, borderRadius: 12, border: '1px solid rgba(148,163,184,.18)', background: '#0f172a', color: '#e2e8f0' }}
              >
                <option value={0}>Select a provider</option>
                {providerOptions.map((provider) => (
                  <option key={provider.id} value={provider.id}>
                    {provider.label}
                  </option>
                ))}
              </select>
            </label>

            <label style={{ display: 'grid', gap: 8 }}>
              <span style={{ color: '#8aa0c7', fontSize: 13 }}>Model Type</span>
              <select
                value={modelType}
                onChange={(event) => setModelType(event.target.value)}
                style={{ padding: 12, borderRadius: 12, border: '1px solid rgba(148,163,184,.18)', background: '#0f172a', color: '#e2e8f0' }}
              >
                <option value="text">text</option>
                <option value="vision">vision</option>
                <option value="embedding">embedding</option>
                <option value="audio">audio</option>
                <option value="chat">chat</option>
              </select>
            </label>
          </div>

          <label style={{ display: 'grid', gap: 8 }}>
            <span style={{ color: '#8aa0c7', fontSize: 13 }}>Model Name</span>
            <input
              value={modelName}
              onChange={(event) => setModelName(event.target.value)}
              placeholder="gemini-2.5-flash"
              style={{ padding: 12, borderRadius: 12, border: '1px solid rgba(148,163,184,.18)', background: '#0f172a', color: '#e2e8f0' }}
            />
          </label>

          <div style={{ display: 'flex', gap: 12, alignItems: 'center', flexWrap: 'wrap' }}>
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
              {createMutation.isPending ? 'Saving...' : 'Add Model'}
            </button>
            {message ? <span style={{ color: '#86efac' }}>{message}</span> : null}
            {error ? <span style={{ color: '#fca5a5' }}>{error}</span> : null}
          </div>
        </form>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, minmax(0, 1fr))', gap: 16 }}>
        <MetricCard label="Models" value={String(data.length)} />
        <MetricCard label="Text Models" value={String(data.filter((row) => row.model_type === 'text').length)} />
        <MetricCard label="Providers" value={String(new Set(data.map((row) => row.provider_id)).size)} />
      </div>
      <DataTable
        data={data}
        columns={[
          { header: 'ID', cell: (row) => String(row.id) },
          { header: 'Provider ID', cell: (row) => String(row.provider_id) },
          { header: 'Model Name', cell: (row) => row.model_name },
          { header: 'Type', cell: (row) => row.model_type },
          { header: 'Created', cell: (row) => new Date(row.created_at).toLocaleString() },
        ]}
      />
    </div>
  )
}
