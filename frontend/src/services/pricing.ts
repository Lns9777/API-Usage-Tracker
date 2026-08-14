import { api } from './api'
import type { PricingCreateInput, PricingRecord } from '../types/pricing'

export const getPricing = async () => (await api.get<PricingRecord[]>('/pricing')).data

export const createPricing = async (payload: PricingCreateInput) => (await api.post<PricingRecord>('/pricing', payload)).data
