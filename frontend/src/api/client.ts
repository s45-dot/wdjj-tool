const BASE_URL = 'http://127.0.0.1:8080'
const DEFAULT_TIMEOUT_MS = 5000

/** In-memory auth token, populated from URL on first access. */
let _authToken: string | null = null

/**
 * Read the token from the URL query parameter ?token=xxx (once).
 * Returns the cached token on subsequent calls.
 */
export function readTokenFromUrl(): string | null {
  if (_authToken !== null) return _authToken
  const params = new URLSearchParams(location.search)
  _authToken = params.get('token') || null
  return _authToken
}

/**
 * Reset the cached auth token (useful for testing or re-auth).
 */
export function clearToken(): void {
  _authToken = null
}

// ── Plain (no-token) helpers ────────────────────────────────────────

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

export async function apiPost<T>(path: string, body: unknown): Promise<T> {
  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT_MS)

  try {
    const res = await fetch(`${BASE_URL}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal: controller.signal,
    })
    if (!res.ok) {
      const text = await res.text()
      throw new Error(`API error: ${res.status} ${text}`)
    }
    return (await res.json()) as T
  } finally {
    clearTimeout(timer)
  }
}

// ── Token-aware helpers ─────────────────────────────────────────────

/**
 * GET request with X-Bubble-Token header.
 * Falls back to plain apiFetch when no token is present.
 */
export async function apiFetchWithToken<T>(path: string): Promise<T> {
  const token = readTokenFromUrl()
  if (!token) return apiFetch<T>(path)

  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT_MS)

  try {
    const res = await fetch(`${BASE_URL}${path}`, {
      headers: { 'X-Bubble-Token': token },
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

/**
 * POST request with X-Bubble-Token header.
 * Falls back to plain apiPost when no token is present.
 */
export async function apiPostWithToken<T>(
  path: string,
  body: unknown,
): Promise<T> {
  const token = readTokenFromUrl()
  if (!token) return apiPost<T>(path, body)

  const controller = new AbortController()
  const timer = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT_MS)

  try {
    const res = await fetch(`${BASE_URL}${path}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Bubble-Token': token,
      },
      body: JSON.stringify(body),
      signal: controller.signal,
    })
    if (!res.ok) {
      const text = await res.text()
      throw new Error(`API error: ${res.status} ${text}`)
    }
    return (await res.json()) as T
  } finally {
    clearTimeout(timer)
  }
}
