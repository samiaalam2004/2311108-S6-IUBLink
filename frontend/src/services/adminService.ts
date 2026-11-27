import { apiData, apiFetch } from "./api"
import type { Post } from "../types/post"
import type { AdminUserRow } from "../types/user"

export const fetchAdminPosts = async (status = "pending") =>
  apiData<Post[]>(await apiFetch(`/api/admin/posts?status=${status}`))

export const reviewPost = async (id: number, status: "approved" | "rejected", note: string) =>
  apiData<Post>(
    await apiFetch(`/api/admin/posts/${id}/review`, {
      method: "PATCH",
      body: JSON.stringify({ status, review_note: note }),
    })
  )

export const fetchAdminUsers = async () =>
  apiData<AdminUserRow[]>(await apiFetch("/api/admin/users"))

export const banUser = async (id: number, isBanned: boolean, reason: string | null) =>
  apiData<AdminUserRow>(
    await apiFetch(`/api/admin/users/${id}/ban`, {
      method: "PATCH",
      body: JSON.stringify({ is_banned: isBanned, ban_reason: reason }),
    })
  )