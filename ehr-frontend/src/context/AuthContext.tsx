import { createContext, useContext, useEffect, useState } from "react"
import { authMe } from "../module/auth/auth.api"

type AuthStatus = "loading" | "authenticated" | "unauthenticated"

type AuthContextType = {
  status: AuthStatus
  doctor: string|undefined
  login: (doctor:string) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [status, setStatus] = useState<AuthStatus>("loading")
  const [doctor, setDoctor] = useState<string>()

  useEffect(() => {
    authMe().then(res => {
      if (res) {
        setStatus("authenticated")
        setDoctor(res.doctor)
      }
      else {
        setStatus("unauthenticated")
        setDoctor("")
      }
    })
      .catch(() => setStatus("unauthenticated"))
  }, [])

  const login = (doctor:string) => {
    setDoctor(doctor)
    setStatus("authenticated")
  }

  const logout = () => {
    setStatus("unauthenticated")
    setDoctor("")
  }

  return (
    <AuthContext.Provider value={{ status, login, logout, doctor }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error("useAuth must be used inside AuthProvider")
  return context
}