import { useMemo, useState, type FormEvent } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { DataTable } from '../components/ui/DataTable'
import { MetricCard } from '../components/ui/MetricCard'
import { PageState } from '../components/ui/PageState'
import { useModels } from '../hooks/useModels'
import { usePricing } from '../hooks/usePricing'
import { createPricing } from '../services/pricing'
import type { PricingCreateInput } from '../types/pricing'

const emptyForm: PricingCreateInput = {
  model_id: 0,
  input_price_per_1m: 0,
  output_price_per_1m: 0,
  thinking_price_per_1m: 0,
  cached_input_price_per_1m: 0,
  currency: 'USD',
  effective_from: new Date().toISOString().slice(0, 16),
  effective_to: null,
}

function toApiDateTime(value: string) {
  return `${value}:00`
}

export default function Pricing() {
  const queryClient = useQueryClient()
  const { data, isLoading, isError } = usePricing()
  const { data: models = [] } = useModels()
  const [form, setForm] = useState<PricingCreateInput>(emptyForm)
  const [message, setMessage] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const createMutation = useMutation({
    mutationFn: createPricing,
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ['pricing'] })
      setMessage('Pricing row added locally and refreshed.')
      setError(null)
      setForm(emptyForm)
    },
    onError: () => {
      setMessage(null)
      setError('Unable to add pricing row. Check the form values and try again.')
    },
  })

  const modelOptions = useMemo(() => models.map((model) => ({ id: model.id, label: `${model.model_name} (#${model.id})` })), [models])

  if (isLoading) {
    return <PageState title="Pricing" description="Loading pricing versions..." />
  }

  if (isError || !data) {
    return <PageState title="Pricing" description="Unable to load pricing." />
  }

  const currentCount = data.filter((row) => !row.effective_to).length
  const uniqueModels = new Set(data.map((row) => row.model_id)).size

  const updateField = (key: keyof PricingCreateInput, value: string | number | null) => {
    setForm((prev) => ({ ...prev, [key]: value as never }))
  }

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setMessage(null)
    setError(null)

    if (!form.model_id) {
      setError('Please select a model.')
      return
    }

    createMutation.mutate({
      ...form,
      effective_from: toApiDateTime(form.effective_from),
      effective_to: form.effective_to ? toApiDateTime(form.effective_to) : null,
    })
  }

  return (
    <div style={{ display: 'grid', gap: 24 }}>
      <div className="page">
        <h1>Pricing</h1>
        <p>Versioned pricing records drive historical cost calculation.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, minmax(0, 1fr))', gap: 16 }}>
        <MetricCard label="Pricing Rows" value={String(data.length)} />
        <MetricCard label="Current" value={String(currentCount)} />
        <MetricCard label="Models Covered" value={String(uniqueModels)} />
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
          <h2 style={{ margin: 0 }}>Add Pricing</h2>
          <p style={{ margin: '6px 0 0', color: '#8aa0c7' }}>
            Create a new versioned pricing row. The new entry is stored locally in your backend database only.
          </p>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'grid', gap: 16 }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, minmax(0, 1fr))', gap: 16 }}>
            <label style={{ display: 'grid', gap: 8 }}>
              <span style={{ color: '#8aa0c7', fontSize: 13 }}>Model</span>
              <select
                value={form.model_id}
                onChange={(event) => updateField('model_id', Number(event.target.value))}
                style={{ padding: 12, borderRadius: 12, border: '1px solid rgba(148,163,184,.18)', background: '#0f172a', color: '#e2e8f0' }}
              >
                <option value={0}>Select a model</option>
                {modelOptions.map((model) => (
                  <option key={model.id} value={model.id}>
                    {model.label}
                  </option>
                ))}
              </select>
            </label>

            <label style={{ display: 'grid', gap: 8 }}>
              <span style={{ color: '#8aa0c7', fontSize: 13 }}>Currency</span>
              <input
                value={form.currency}
                onChange={(event) => updateField('currency', event.target.value.toUpperCase())}
                style={{ padding: 12, borderRadius: 12, border: '1px solid rgba(148,163,184,.18)', background: '#0f172a', color: '#e2e8f0' }}
              />
            </label>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, minmax(0, 1fr))', gap: 16 }}>
            {[
              ['input_price_per_1m', 'Input / 1M'],
              ['output_price_per_1m', 'Output / 1M'],
              ['thinking_price_per_1m', 'Thinking / 1M'],
              ['cached_input_price_per_1m', 'Cached / 1M'],
            ].map(([key, label]) => (
              <label key={key} style={{ display: 'grid', gap: 8 }}>
                <span style={{ color: '#8aa0c7', fontSize: 13 }}>{label}</span>
                <input
                  type="number"
                  step="0.0001"
                  min="0"
                  value={form[key as keyof PricingCreateInput] as number}
                  onChange={(event) => updateField(key as keyof PricingCreateInput, Number(event.target.value))}
                  style={{ padding: 12, borderRadius: 12, border: '1px solid rgba(148,163,184,.18)', background: '#0f172a', color: '#e2e8f0' }}
                />
              </label>
            ))}
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, minmax(0, 1fr))', gap: 16 }}>
            <label style={{ display: 'grid', gap: 8 }}>
              <span style={{ color: '#8aa0c7', fontSize: 13 }}>Effective From</span>
              <input
                type="datetime-local"
                value={form.effective_from}
                onChange={(event) => updateField('effective_from', event.target.value)}
                style={{ padding: 12, borderRadius: 12, border: '1px solid rgba(148,163,184,.18)', background: '#0f172a', color: '#e2e8f0' }}
              />
            </label>

            <label style={{ display: 'grid', gap: 8 }}>
              <span style={{ color: '#8aa0c7', fontSize: 13 }}>Effective To</span>
              <input
                type="datetime-local"
                value={form.effective_to ?? ''}
                onChange={(event) => updateField('effective_to', event.target.value || null)}
                style={{ padding: 12, borderRadius: 12, border: '1px solid rgba(148,163,184,.18)', background: '#0f172a', color: '#e2e8f0' }}
              />
            </label>
          </div>

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
              {createMutation.isPending ? 'Saving...' : 'Add Pricing'}
            </button>
            {message ? <span style={{ color: '#86efac' }}>{message}</span> : null}
            {error ? <span style={{ color: '#fca5a5' }}>{error}</span> : null}
          </div>
        </form>
      </div>

      <DataTable
        data={data}
        columns={[
          { header: 'Model ID', cell: (row) => String(row.model_id) },
          { header: 'Input / 1M', cell: (row) => `$${row.input_price_per_1m.toFixed(4)}` },
          { header: 'Output / 1M', cell: (row) => `$${row.output_price_per_1m.toFixed(4)}` },
          { header: 'Thinking / 1M', cell: (row) => `$${row.thinking_price_per_1m.toFixed(4)}` },
          { header: 'Cached / 1M', cell: (row) => `$${row.cached_input_price_per_1m.toFixed(4)}` },
          { header: 'Currency', cell: (row) => row.currency },
          { header: 'Effective From', cell: (row) => new Date(row.effective_from).toLocaleString() },
          { header: 'Effective To', cell: (row) => row.effective_to ? new Date(row.effective_to).toLocaleString() : 'Current' },
        ]}
      />
    </div>
  )
}
