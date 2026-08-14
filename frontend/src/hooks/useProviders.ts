import { useQuery } from '@tanstack/react-query'
import { getProviders } from '../services/providers'

export const useProviders = () => useQuery({ queryKey: ['providers'], queryFn: getProviders })
