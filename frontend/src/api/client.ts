import axios from 'axios'

const client = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
})

export interface Skill {
  id: string
  name: string
  version: string
  author: string
  description: string
  tags: string[]
  downloads: number
  created_at: string
  updated_at: string
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  limit: number
}

export interface Stats {
  skills: number
  authors: number
  installs: number
}

export interface SkillCreate {
  name: string
  version?: string
  author: string
  description?: string
  tags?: string[]
}

export async function searchSkills(q: string, page = 1, limit = 20, sort = 'downloads'): Promise<PaginatedResponse<Skill>> {
  const { data } = await client.get('/skills', { params: { q, page, limit, sort } })
  return data
}

export async function getSkill(name: string): Promise<Skill> {
  const { data } = await client.get(`/skills/${name}`)
  return data
}

export async function createSkill(skill: SkillCreate): Promise<Skill> {
  const { data } = await client.post('/skills', skill)
  return data
}

export async function getStats(): Promise<Stats> {
  const { data } = await client.get('/stats')
  return data
}
