import type { Patient } from "../patient/patient.type"


export type ChatRequest = {
    query:string
    patientId: string|undefined
}

export type ChatContainerProps = {
    patient:Patient | undefined
}

export type ChatMessage = {
    isAIGenerated:boolean
    text: string
    thinking: boolean
}

export type ChatHistoryMessageProps = {
    chatMessage: ChatMessage
}

export type ChatHistoryProps = {
    History: ChatMessage[]
}

export type ChatInputProps = {
    History: ChatMessage[]
    AddNewMessage: (message:ChatMessage) => void
    patient?: Patient
    updatedAnswer: (message:string) => void
}