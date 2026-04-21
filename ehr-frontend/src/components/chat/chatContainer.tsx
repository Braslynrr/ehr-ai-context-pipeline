import { useState } from "react";
import type { ChatContainerProps, ChatMessage } from "../../module/chat/chat.types";
import ChatHistory from "./chatHistory";
import ChatInput from "./chatInput";
import type { Patient } from "../../module/patient/patient.type";
import { streamEvent } from "../../client/streaming_client";

export default function ChatContainer({ patient }: ChatContainerProps) {

    const [history, setHistory] = useState<ChatMessage[]>([])

    function onNewStream(id: string, patient: Patient | undefined) {
        const aiMessage: ChatMessage = { isAIGenerated: true, text: "", thinking: true, patient }
        setHistory((prev) => [...prev, aiMessage])
        streamEvent("/ehr/stream/", id, updateLastChatMessage, onErrorChatMessage)
    }

    function onErrorChatMessage({ error }: { error: string }) {
        setHistory(prev => {
            if (prev.length < 2) return prev

            const userIndex = prev.length - 2
            const aiIndex = prev.length - 1

            const newHistory = prev.slice(0, aiIndex)

            newHistory[userIndex] = {
                ...newHistory[userIndex],
                error
            }

            return newHistory
        })
    }
    
    let buffer = ""

    function updateLastChatMessage({ chunk, thinking }: { chunk: string, thinking?: boolean }) {

        if (chunk !== "[DONE]" && !thinking) {
            buffer += chunk

            if (buffer.length > 20) {
                flush()
            }

        } else if (thinking) {

            setHistory(prev => {
                if (prev.length === 0) return prev
                const lastIndex = prev.length - 1

                return [
                    ...prev.slice(0, lastIndex),
                    {
                        ...prev[lastIndex],
                        thinking: true,
                        thinkingContext: chunk
                    }
                ]
            })

        } else {
            flush()
            buffer = ""
        }
    }

    function onErrorMessage(error: string) {
        setHistory(prev => {
            if (prev.length === 0) return prev
            const lastIndex = prev.length - 1


            console.log(prev[lastIndex])
            return [
                ...prev.slice(0, lastIndex),
                {
                    ...prev[lastIndex],
                    error: error
                }
            ]
        })
    }

    function flush() {
        const content = buffer
        buffer = ""

        setHistory(prev => {
            if (prev.length === 0) return prev
            const lastIndex = prev.length - 1

            return [
                ...prev.slice(0, lastIndex),
                {
                    ...prev[lastIndex],
                    text: prev[lastIndex].text + content,
                    thinking: false
                }
            ]
        })
    }

    return <div className="flex-1 min-h-0 flex flex-col">
        <div className="flex-[8] overflow-y-auto min-h-0 bg-gray-700">
            <ChatHistory History={history} />
        </div>

        <div className="flex-[2] bg-gray-700">
            <ChatInput
                patient={patient}
                History={history}
                onError={onErrorMessage}
                newStream={onNewStream} AddNewMessage={(message) => setHistory((prev) => [...prev, message])} />
        </div>
    </div>

}