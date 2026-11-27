import { apiData, apiFetch } from "./api"
import type { User } from "../types/user"

export const fetchCurrentUser = async () =>
  apiData<User>(await apiFetch("/api/auth/me"))

export const updateProfile = async (body: object) =>
  apiData<User>(
    await apiFetch("/api/users/me", { method: "PATCH", body: JSON.stringify(body) })
  )

export const changePassword = async (current_password: string, new_password: string) =>
  apiData<{ message: string }>(
    await apiFetch("/api/users/me/change-password", {
      method: "POST",
      body: JSON.stringify({ current_password, new_password }),
    })
  )