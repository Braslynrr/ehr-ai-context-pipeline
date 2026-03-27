import React, { useState } from "react"
import { useAuth } from "../../context/AuthContext"
import { useNavigate } from "react-router-dom"
import { authLogin } from "../../module/auth/auth.api"


export default function Login() {
  const [doctor, setDoctor] = useState("")
  const { login } = useAuth()
  const navigate = useNavigate()

  async function handleLogin(e: React.SubmitEvent) {
    e.preventDefault()
    await authLogin({ doctor })
    login()
    navigate("/chat")
  }


  return (
    <form
      onSubmit={handleLogin}
      className="flex flex-col gap-4 bg-white border border-gray-200 shadow-sm rounded-2xl px-10 py-8 w-full max-w-sm">
      <h1 className="text-xl font-semibold text-gray-800 text-center">
        Medical Assistant
      </h1>

      <p className="text-sm text-gray-500 text-center">
        Enter your name to continue
      </p>

      <input
        className="border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Doctor name"
        value={doctor}
        onChange={(e) => setDoctor(e.currentTarget.value)}
        required />

      <button className="bg-blue-600 hover:bg-blue-700 text-white rounded-lg py-2 font-medium transition">
        Enter
      </button>
    </form>)

}