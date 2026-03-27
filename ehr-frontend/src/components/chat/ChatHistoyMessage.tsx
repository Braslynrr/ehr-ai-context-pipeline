import ReactMarkdown from "react-markdown";
import type { ChatHistoryMessageProps } from "../../module/chat/chat.types";


export default function ChatHistoyMessage({ chatMessage }: ChatHistoryMessageProps) {

    if (!chatMessage.isAIGenerated)
        return <div className="flex flex-col gap-2 bg-gray-600 text-white borde shadow-sm rounded-xl px-12 py-3 w-full max-w-xs self-end">
            <p>
                {chatMessage.text}
            </p>
        </div>

    return (
        <div className="w-full flex justify-center px-4 py-3">
            <div className="w-full max-w-2xl text-gray-200">
                {chatMessage.thinking ? (
                    <span className="animate-pulse">
                        Thinking...
                    </span>
                ) : (
                    <div className="prose prose-sm max-w-none">
                        <ReactMarkdown>
                            {chatMessage.text}
                        </ReactMarkdown>
                    </div>
                )}
            </div>
        </div>
    )

}