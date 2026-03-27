import Header from "../components/header/header"
import Login from "../components/login/login"

export default function LoginPage() {

  return (
    <div className="flex flex-col h-screen bg-gray-50 text-gray-900">
      <Header />
      <main className="flex-1 flex items-center justify-center">
        <Login />
      </main>
    </div>
  )
}