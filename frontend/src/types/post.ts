export type PostType = "job_seeking" | "job" | "internship"

export interface Post {
  id: number
  title: string
  description: string
  post_type: PostType
  company: string | null
  owner_id: number | string
  owner_name: string
  status: string
  review_note: string | null
  created_at: string
}