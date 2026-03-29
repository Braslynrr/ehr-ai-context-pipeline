import { useState } from "react";
import type { ChatInputProps } from "../../module/chat/chat.types";
import { getStream } from "../../module/chat/chat.api";


export default function ChatInput({ AddNewMessage, newStream , patient }: ChatInputProps) {

    const [query, setQuery] = useState("")
    const [isAnswering, setIsAnswering] = useState(false)

    const handleQuery = async () => {
        setIsAnswering(true)
        setQuery("")
        getStream({query, patientId:patient?.patient_id})
        .then((id)=>{
            AddNewMessage({ isAIGenerated: false, text: query, thinking: false, patient })
            newStream(id, patient)
        })
        .catch()
        setIsAnswering(false)
    }


    return (
        <div className="w-full flex justify-center p-4">
            <div className="w-full max-w-2xl bg-gray-800 rounded-2xl shadow-md flex items-end gap-2 p-3">

                <textarea
                    value={query}
                    onChange={(e) => setQuery(e.currentTarget.value)}
                    onInput={(e) => {
                        e.currentTarget.style.height = "auto"
                        e.currentTarget.style.height = e.currentTarget.scrollHeight + "px"
                    }}
                    placeholder={!patient? "Ask anything": `Ask anything about ${patient.name}`}
                    className="flex-1 resize-none bg-transparent text-white outline-none placeholder-gray-400 max-h-40"
                />

                <button
                    onClick={handleQuery}
                    disabled={isAnswering}
                    className="bg-blue-600 hover:bg-blue-500 disabled:bg-gray-600 text-white px-4 py-2 rounded-xl"
                >
                    {isAnswering ? "..." : "Ask"}
                </button>

                {isAnswering && (
                    <button
                        className="bg-red-500 hover:bg-red-400 text-white px-3 py-2 rounded-xl"
                    >
                        Stop
                    </button>
                )}
            </div>
        </div>
    )
}