const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

let accessToken = null;

export function setAccessToken(token) {
  accessToken = token;
}

export function getAccessToken() {
  return accessToken;
}

export async function refreshSession() {
  const res = await fetch(`${API_BASE_URL}/api/auth/refresh`, {
    method: "POST",
    credentials: "include",
  });

  if (!res.ok) {
    setAccessToken(null);
    return null;
  }

  const data = await res.json();
  setAccessToken(data.access_token);
  return data.access_token;
}

export async function apiFetch(path, options = {}, retry = true) {
  const headers = new Headers(options.headers || {});
  if (options.body && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  if (accessToken) {
    headers.set("Authorization", `Bearer ${accessToken}`);
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
    credentials: "include",
  });

  if (response.status === 401 && retry && !path.startsWith("/api/auth/")) {
    const newToken = await refreshSession();
    if (newToken) {
      return apiFetch(path, options, false);
    }
  }

  return response;
}