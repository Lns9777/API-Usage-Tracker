export type UsageRecord = {
  id: number
  project_id: number
  provider_id: number
  model_id: number
  internal_request_id: string
  provider_request_id?: string | null
  timestamp: string
  input_tokens: number
  output_tokens: number
  thinking_tokens: number
  cached_tokens: number
  total_tokens: number
  input_cost: number
  output_cost: number
  thinking_cost: number
  cached_cost: number
  total_cost: number
  latency_ms: number
  status: string
  http_status_code?: number | null
  error_type?: string | null
  metadata_json?: Record<string, unknown>
  capture_content?: boolean
}
