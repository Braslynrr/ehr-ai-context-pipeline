import { Navigate } from "react-router-dom"
import type { JSX } from "react"
import { useAuth } from "../../context/AuthContext"

export default function ProtectedRoute({ children }: { children: JSX.Element }) {
  const { status } = useAuth()

  if (status === "loading") {
    return <div>Loading...</div>
  }

  if (status === "unauthenticated") {
    return <Navigate to="/" replace />
  }

  return children
}