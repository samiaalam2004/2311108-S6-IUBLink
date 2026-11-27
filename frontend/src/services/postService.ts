import { apiData, apiFetch } from "./api"
import type { Post } from "../types/post"

export const fetchApprovedPosts = async () =>
  apiData<Post[]>(await apiFetch("/api/posts"))

export const fetchPost = async (id: number) =>
  apiData<Post>(await apiFetch(`/api/posts/${id}`))

export const fetchMyPosts = async () =>
  apiData<Post[]>(await apiFetch("/api/my-posts"))

export const createPost = async (body: object) =>
  apiData<Post>(
    await apiFetch("/api/posts", { method: "POST", body: JSON.stringify(body) })
  )

export const updatePost = async (id: number, body: object) =>
  apiData<Post>(
    await apiFetch(`/api/posts/${id}`, { method: "PATCH", body: JSON.stringify(body) })
  )

export const deletePost = async (id: number) =>
  apiData<{ message: string }>(
    await apiFetch(`/api/posts/${id}`, { method: "DELETE" })
  )