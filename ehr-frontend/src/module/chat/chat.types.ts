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
    patient?: Patient
    error?: string
    thinkingContext?:string
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
    newStream: (message:string, patient:Patient|undefined) => void
    onError: (error:string) => void
}