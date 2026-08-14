import { useQuery } from '@tanstack/react-query'
import { getOverview } from '../services/analytics'

export const useAnalytics = () => useQuery({ queryKey: ['overview'], queryFn: getOverview })
