import { api } from './api'
import type { Project } from '../types/project'

export const getProjects = async () => (await api.get<Project[]>('/projects')).data
