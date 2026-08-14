import { api } from './api'
import type { UsageRecord } from '../types/usage'

export const getUsage = async () => (await api.get<UsageRecord[]>('/usage')).data
