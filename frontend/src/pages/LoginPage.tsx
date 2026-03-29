import { FormEvent, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/client'
import { useAuth } from '../context/AuthContext'

export function LoginPage() {
  const [email, setEmail] = useState('admin@example.com')
  const [password, setPassword] = useState('password123')
  const [error, setError] = useState('')
  const { setToken } = useAuth()
  const navigate = useNavigate()

  const submit = async (event: FormEvent) => {
    event.preventDefault()
    try {
      const response = await api.post('/auth/login', { email, password })
      setToken(response.data.access_token)
      navigate('/dashboard')
    } catch {
      setError('Login failed. Check credentials.')
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-100">
      <form onSubmit={submit} className="w-full max-w-md space-y-3 rounded-xl bg-white p-8 shadow">
        <h1 className="text-2xl font-bold">AI Task Allocation</h1>
        <input className="w-full rounded border p-2" value={email} onChange={(e) => setEmail(e.target.value)} />
        <input
          className="w-full rounded border p-2"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          type="password"
        />
        {error && <p className="text-sm text-red-500">{error}</p>}
        <button className="w-full rounded bg-brand py-2 text-white">Login</button>
      </form>
    </main>
  )
}
