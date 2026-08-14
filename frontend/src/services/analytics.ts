import { api } from './api'
import type { OverviewStats } from '../types/analytics'

export const getOverview = async () => (await api.get<OverviewStats>('/analytics/overview')).data
