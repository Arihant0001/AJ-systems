type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'

export class ApiError extends Error {
  status: number
  constructor(status: number, message: string) {
    super(message)
    this.status = status
  }
}

function getBaseUrl() {
  const base = import.meta.env.VITE_API_URL
  return base?.replace(/\/$/, '')
}

export async function apiRequest<T>(
  path: string,
  options?: {
    method?: HttpMethod
    token?: string | null
    body?: unknown
    responseType?: 'json' | 'blob'
  },
): Promise<T> {
  const baseUrl = getBaseUrl()
  const url = `${baseUrl}${path.startsWith('/') ? path : `/${path}`}`
  const method = options?.method ?? 'GET'

  const headers: Record<string, string> = {}
  if (options?.token) headers.Authorization = `Bearer ${options.token}`

  let body: BodyInit | undefined
  if (options?.body !== undefined) {
    headers['Content-Type'] = 'application/json'
    body = JSON.stringify(options.body)
  }

  const res = await fetch(url, { method, headers, body })

  if (!res.ok) {
    let message = `Request failed (${res.status})`
    try {
      const data = await res.json()
      if (typeof data?.detail === 'string') message = data.detail
    } catch {
      // ignore
    }
    throw new ApiError(res.status, message)
  }

  if ((options?.responseType ?? 'json') === 'blob') {
    return (await res.blob()) as T
  }

  // Some endpoints may return 204
  if (res.status === 204) return undefined as T
  return (await res.json()) as T
}
