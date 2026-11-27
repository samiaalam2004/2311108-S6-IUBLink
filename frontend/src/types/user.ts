export interface User {
  id: number
  full_name: string
  email: string
  role: string
  department?: string | null
  batch_or_graduation?: string | null
  headline?: string | null
  bio?: string | null
  linkedin_url?: string | null
  is_banned?: boolean
  ban_reason?: string | null
}

export interface AdminUserRow {
  id: number
  full_name: string
  email: string
  role: string
  department?: string | null
  batch_or_graduation?: string | null
  is_banned: boolean
  ban_reason?: string | null
}