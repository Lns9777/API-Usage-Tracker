import { useQuery } from '@tanstack/react-query'
import { getProjects } from '../services/projects'

export const useProjects = () => useQuery({ queryKey: ['projects'], queryFn: getProjects })
