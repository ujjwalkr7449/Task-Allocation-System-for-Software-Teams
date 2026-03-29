import { createContext, ReactNode, useContext, useEffect, useMemo, useState } from 'react'

interface AuthContextValue {
  token: string | null
  setToken: (token: string | null) => void
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setTokenState] = useState<string | null>(localStorage.getItem('token'))

  const setToken = (nextToken: string | null) => {
    setTokenState(nextToken)
    if (nextToken) {
      localStorage.setItem('token', nextToken)
    } else {
      localStorage.removeItem('token')
    }
  }

  useEffect(() => {
    const existing = localStorage.getItem('token')
    if (existing) setTokenState(existing)
  }, [])

  const value = useMemo(() => ({ token, setToken }), [token])
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}
