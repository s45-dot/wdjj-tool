import { apiFetch } from './client'

export interface HealthResponse {
  ok: boolean
  version: string
}

export async function getHealth(): Promise<HealthResponse> {
  return apiFetch<HealthResponse>('/api/health')
}
