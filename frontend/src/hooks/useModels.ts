import { useQuery } from '@tanstack/react-query'
import { getModels } from '../services/models'

export const useModels = () => useQuery({ queryKey: ['models'], queryFn: getModels })
