import { useEffect, useState } from 'react'
import api from '../api/client'
import { KanbanBoard } from '../components/KanbanBoard'
import { NotificationPanel } from '../components/NotificationPanel'
import { ProjectForm } from '../components/ProjectForm'
import { Notification, Project, Task, TaskStatus } from '../types'

export function DashboardPage() {
  const [projects, setProjects] = useState<Project[]>([])
  const [activeProjectId, setActiveProjectId] = useState<number | null>(null)
  const [tasks, setTasks] = useState<Task[]>([])
  const [notifications, setNotifications] = useState<Notification[]>([])

  async function loadProjects() {
    const response = await api.get<Project[]>('/projects')
    setProjects(response.data)
    if (response.data.length > 0 && !activeProjectId) {
      setActiveProjectId(response.data[0].id)
    }
  }

  async function loadTasks(projectId: number) {
    const response = await api.get<Task[]>(`/projects/${projectId}/tasks`)
    setTasks(response.data)
  }

  async function loadNotifications() {
    const response = await api.get<Notification[]>('/notifications/me')
    setNotifications(response.data)
  }

  async function createProject(payload: { name: string; description: string; requirements_text: string }) {
    const project = await api.post<Project>('/projects', payload)
    await api.post(`/projects/${project.data.id}/ai-breakdown`)
    await loadProjects()
    setActiveProjectId(project.data.id)
  }

  async function updateTaskStatus(taskId: number, status: TaskStatus) {
    await api.patch(`/tasks/${taskId}/status`, { status })
    if (activeProjectId) await loadTasks(activeProjectId)
  }

  useEffect(() => {
    loadProjects()
    loadNotifications()
  }, [])

  useEffect(() => {
    if (activeProjectId) {
      loadTasks(activeProjectId)
    }
  }, [activeProjectId])

  return (
    <main className="min-h-screen bg-slate-100 p-6">
      <header className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-bold">Project Dashboard</h1>
        <select
          className="rounded border p-2"
          value={activeProjectId ?? ''}
          onChange={(e) => setActiveProjectId(Number(e.target.value))}
        >
          {projects.map((project) => (
            <option key={project.id} value={project.id}>
              {project.name}
            </option>
          ))}
        </select>
      </header>

      <div className="mb-4 grid gap-4 lg:grid-cols-2">
        <ProjectForm onCreate={createProject} />
        <NotificationPanel items={notifications} />
      </div>

      <KanbanBoard tasks={tasks} onStatusChange={updateTaskStatus} />
    </main>
  )
}
