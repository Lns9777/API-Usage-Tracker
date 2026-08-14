import { api } from './api'
import type { Provider } from '../types/provider'

export const getProviders = async () => (await api.get<Provider[]>('/providers')).data

export const createProvider = async (name: string) => (await api.post<Provider>('/providers', { name })).data
