export type UserRole = 'ADMIN' | 'FRONTEND' | 'BACKEND' | 'DESIGNER'
export type TaskStatus = 'TODO' | 'IN_PROGRESS' | 'DONE'

export interface User {
  id: number
  full_name: string
  email: string
  role: UserRole
  skills: string
}

export interface Project {
  id: number
  name: string
  description: string
  requirements_text: string
  created_by_id: number
  created_at: string
}

export interface Task {
  id: number
  title: string
  description: string
  required_role: UserRole
  status: TaskStatus
  priority: string
  project_id: number
  assignee_id: number | null
  created_at: string
}

export interface Notification {
  id: number
  user_id: number
  message: string
  is_read: boolean
  created_at: string
}
