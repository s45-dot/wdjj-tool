const BASE_URL = 'http://127.0.0.1:8080'
const DEFAULT_TIMEOUT_MS = 5000

export async function apiFetch<T>(path: string): Promise<T> {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT_MS)

  try {
    const res = await fetch(`${BASE_URL}${path}`, {
      signal: controller.signal,
    })
    if (!res.ok) {
      throw new Error(`API error: ${res.status} ${res.statusText}`)
    }
    return (await res.json()) as T
  } finally {
    clearTimeout(timer)
  }
}
