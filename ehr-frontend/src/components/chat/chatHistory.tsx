import type { ChatHistoryProps } from "../../module/chat/chat.types"
import ChatHistoyMessage from "./ChatHistoyMessage"


export default function ChatHistory({ History }:ChatHistoryProps) {

    return <div className="flex flex-col min-h-0">
        {History.map((message, index) => <ChatHistoyMessage key={index} chatMessage={message} />)}
    </div>

}