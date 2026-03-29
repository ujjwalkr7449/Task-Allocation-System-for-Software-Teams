import { Notification } from '../types'

export function NotificationPanel({ items }: { items: Notification[] }) {
  return (
    <div className="rounded-xl bg-white p-4 shadow">
      <h2 className="mb-3 text-lg font-semibold">Notifications</h2>
      <div className="space-y-2">
        {items.length === 0 && <p className="text-sm text-slate-500">No notifications.</p>}
        {items.map((item) => (
          <div key={item.id} className="rounded border p-2 text-sm">
            <p>{item.message}</p>
            <p className="text-xs text-slate-500">{new Date(item.created_at).toLocaleString()}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
