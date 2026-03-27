import { useState } from "react";
import type { ChatContainerProps, ChatMessage } from "../../module/chat/chat.types";
import ChatHistory from "./chatHistory";
import ChatInput from "./chatInput";

export default function ChatContainer({ patient }: ChatContainerProps) {

    const [history, setHistory] = useState<ChatMessage[]>([])

    function updateLastChatMessage(text: string) {
        setHistory((prev) => {
            if (prev.length === 0) return prev

            let updated = [...prev]

            updated[updated.length - 1] = {
                isAIGenerated:true,
                text: updated[updated.length - 1].text + text,
                thinking:false
            }

            return updated
        })
    }

    return <div className="h-screen flex flex-col">
        <div className="flex-[8] overflow-y-auto bg-gray-700">
            <ChatHistory History={history} />
        </div>

        <div className="flex-[2] bg-gray-700">
            <ChatInput
            patient={patient} 
            History={history} 
            updatedAnswer={updateLastChatMessage} AddNewMessage={(message) => setHistory((prev) => [...prev, message])} />
        </div>
    </div>

}