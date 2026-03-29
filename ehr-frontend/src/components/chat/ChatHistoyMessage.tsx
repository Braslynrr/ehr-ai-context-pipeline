import ReactMarkdown from "react-markdown";
import type { ChatHistoryMessageProps } from "../../module/chat/chat.types";


export default function ChatHistoyMessage({ chatMessage }: ChatHistoryMessageProps) {

    if (!chatMessage.isAIGenerated)
        return <div className="flex flex-col gap-2 bg-gray-600 text-white borde shadow-sm rounded-xl px-12 py-3 w-full max-w-xs self-end">
            {chatMessage.patient && (
                <div className="text-xs text-gray-300 mb-1">
                    Patient: {chatMessage.patient.name}
                </div>
            )}

            <p className="break-words whitespace-pre-wrap">{chatMessage.text}</p>

            {chatMessage.error && (
                <div className="text-red-400 text-sm mt-1">
                    ⚠ {chatMessage.error}
                </div>
            )}
        </div>

    return (
        <div className="w-full flex justify-center px-4 py-3">
            <div className="w-full max-w-2xl text-gray-200">
                {chatMessage.thinking ? (
                    <span className="animate-pulse">
                        Thinking...
                    </span>
                ) : (
                    <div className="max-w-none">
                        <ReactMarkdown>
                            {chatMessage.text}
                        </ReactMarkdown>
                    </div>
                )}
            </div>
        </div>
    )

}