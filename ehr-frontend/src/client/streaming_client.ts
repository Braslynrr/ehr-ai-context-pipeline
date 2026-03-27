import type { ChatRequest } from "../module/chat/chat.types"

const BASE_URL = import.meta.env.VITE_EHR_API_URL

export async function streamFetch(
  endpoint: string,
  body: ChatRequest,
  onChunk: (chunk: string) => void
) {
  const res = await fetch(BASE_URL + endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
    body: JSON.stringify(body),
  })

  const reader = res.body!.getReader()
  const decoder = new TextDecoder()

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    onChunk(decoder.decode(value))
  }
}