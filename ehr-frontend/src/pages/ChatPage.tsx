import { useState } from "react"
import Header from "../components/header/header"
import ChatContainer from "../components/chat/chatContainer"
import PatientPanel from "../components/patient/patient.panel"
import type { Patient } from "../module/patient/patient.type"
import { useAuth } from "../context/AuthContext"


export default function ChatPage() {
  const [patient, setPatient] = useState<Patient>()
  const {doctor} = useAuth()

  return (
    <div className="flex h-screen bg-gray-100 text-black">
      <aside className="border-r">
        <PatientPanel patient={patient} onSelect={setPatient} />
      </aside>
      <main className="flex-1 flex flex-col">
        <Header doctor={doctor} />
        <ChatContainer patient={patient}  />
      </main>
    </div>)
}