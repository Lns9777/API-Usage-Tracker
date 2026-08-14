import { useQuery } from '@tanstack/react-query'
import { getUsage } from '../services/usage'

export const useUsage = () => useQuery({ queryKey: ['usage'], queryFn: getUsage })
