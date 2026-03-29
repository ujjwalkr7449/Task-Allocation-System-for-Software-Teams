import { Task, TaskStatus } from '../types'

const columns: Array<{ key: TaskStatus; title: string }> = [
  { key: 'TODO', title: 'To Do' },
  { key: 'IN_PROGRESS', title: 'In Progress' },
  { key: 'DONE', title: 'Done' },
]

interface KanbanBoardProps {
  tasks: Task[]
  onStatusChange: (taskId: number, status: TaskStatus) => void
}

export function KanbanBoard({ tasks, onStatusChange }: KanbanBoardProps) {
  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-3">
      {columns.map((column) => (
        <div key={column.key} className="rounded-xl bg-white p-4 shadow">
          <h3 className="mb-3 font-semibold text-slate-800">{column.title}</h3>
          <div className="space-y-3">
            {tasks
              .filter((task) => task.status === column.key)
              .map((task) => (
                <div key={task.id} className="rounded-lg border border-slate-200 p-3">
                  <p className="font-medium">{task.title}</p>
                  <p className="text-sm text-slate-500">{task.required_role}</p>
                  <div className="mt-2 flex gap-2">
                    {columns.map((statusOption) => (
                      <button
                        key={statusOption.key}
                        className="rounded bg-slate-100 px-2 py-1 text-xs hover:bg-slate-200"
                        onClick={() => onStatusChange(task.id, statusOption.key)}
                      >
                        {statusOption.title}
                      </button>
                    ))}
                  </div>
                </div>
              ))}
          </div>
        </div>
      ))}
    </div>
  )
}
