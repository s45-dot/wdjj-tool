import { apiFetchWithToken } from './client'

export interface NetworkInfo {
  host: string
  port: number
  url: string
}

/**
 * Fetch LAN network information (host, port, URL).
 * Attaches the auth token automatically when present.
 */
export async function getNetworkInfo(): Promise<NetworkInfo> {
  return apiFetchWithToken<NetworkInfo>('/api/network')
}
