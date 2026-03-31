import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm"
import type { ChatHistoryMessageProps } from "../../module/chat/chat.types";


export default function ChatHistoyMessage({ chatMessage }: ChatHistoryMessageProps) {

    const content = chatMessage.text.replace(/\|\s*\|/g, "|\n|")

    if (!chatMessage.isAIGenerated)
        return <div className="flex flex-col gap-2 bg-gray-600 text-white borde shadow-sm rounded-xl px-12 py-3 w-full max-w-xs self-end">

            <div className="text-xs text-gray-300 mb-1">
                {chatMessage.patient ? `Patient: ${chatMessage.patient.name}` : "global query"}
            </div>


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
                        <ReactMarkdown remarkPlugins={[remarkGfm]}
                            components={
                                {
                                    table: (props) => (
                                        <table className="table-auto w-full text-sm py-2" {...props} />
                                    ),
                                    th: (props) => (
                                        <th className="px-3 py-2 bg-gray-900 text-left" {...props} />
                                    ),
                                    td: (props) => (
                                        <td className="bg-gray-800 px-3 py-2" {...props} />
                                    ),
                                    p: (props) => (
                                        <p className="py-1" {...props} />)
                                }
                            }>
                            {content}
                        </ReactMarkdown>
                    </div>
                )}
            </div>
        </div>
    )

}