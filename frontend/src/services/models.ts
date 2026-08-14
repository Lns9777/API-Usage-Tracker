import { api } from './api'
import type { Model } from '../types/model'

export const getModels = async () => (await api.get<Model[]>('/models')).data

export const createModel = async (payload: { provider_id: number; model_name: string; model_type: string }) =>
  (await api.post<Model>('/models', payload)).data
