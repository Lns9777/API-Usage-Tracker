export type PricingRecord = {
  id: number
  model_id: number
  input_price_per_1m: number
  output_price_per_1m: number
  thinking_price_per_1m: number
  cached_input_price_per_1m: number
  currency: string
  effective_from: string
  effective_to?: string | null
  created_at: string
  updated_at: string
}

export type PricingCreateInput = {
  model_id: number
  input_price_per_1m: number
  output_price_per_1m: number
  thinking_price_per_1m: number
  cached_input_price_per_1m: number
  currency: string
  effective_from: string
  effective_to?: string | null
}
