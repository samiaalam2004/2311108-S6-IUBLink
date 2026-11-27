const API_BASE_URL: string = (
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"
).replace(/\/$/, "")

let accessToken: string | null = null

export function setAccessToken(token: string | null) {
  accessToken = token
}

export function getAccessToken() {
  return accessToken
}

// পুরনো নাম, যাতে App.tsx ভাঙে না
export const setStoredToken = setAccessToken
export const getStoredToken = getAccessToken

// একসাথে অনেক request 401 পেলে refresh একবারই হবে
let refreshing: Promise<string | null> | null = null

export function refreshSession(): Promise<string | null> {
  if (!refreshing) {
    refreshing = (async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/api/auth/refresh`, {
          method: "POST",
          credentials: "include",
        })
        if (!res.ok) {
          setAccessToken(null)
          return null
        }
        const data = await res.json()
        setAccessToken(data.access_token)
        return data.access_token as string
      } catch {
        setAccessToken(null)
        return null
      } finally {
        refreshing = null
      }
    })()
  }
  return refreshing
}

export const refreshAccessToken = refreshSession

export async function apiFetch(
  path: string,
  options: RequestInit = {},
  retry = true
): Promise<Response> {
  const headers = new Headers(options.headers || {})
  if (options.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json")
  }
  if (accessToken) {
    headers.set("Authorization", `Bearer ${accessToken}`)
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
    credentials: "include",
  })

  if (response.status === 401 && retry && !path.startsWith("/api/auth/")) {
    const newToken = await refreshSession()
    if (newToken) {
      return apiFetch(path, options, false)
    }
  }

  return response
}

// response থেকে JSON নেয়, ব্যর্থ হলে সুন্দর error message দিয়ে throw করে
export async function apiData<T>(response: Response): Promise<T> {
  let body: any = null
  try {
    body = await response.json()
  } catch {
    body = null
  }

  if (!response.ok) {
    let message = `Request failed (${response.status})`
    if (body && typeof body.detail === "string") {
      message = body.detail
    } else if (body && Array.isArray(body.detail) && body.detail[0]?.msg) {
      message = body.detail[0].msg
    }
    throw new Error(message)
  }

  return body as T
}