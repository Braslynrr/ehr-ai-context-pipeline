const BASE_URL = import.meta.env.VITE_EHR_API_URL

export async function streamEvent(
  endpoint: string,
  id: string,
  onChunk: ({ chunk }: { chunk: string }) => void,
  onErrorChatMessage: ({ error }: { error: string }) => void
) {

  const evtSource = new EventSource(`${BASE_URL}${endpoint}${id}`, { withCredentials: true })

  evtSource.onmessage = (event) => {

    const data = JSON.parse(event.data)
    onChunk(data)

    if (data.chunk === "[DONE]") {
      evtSource.close()
      return
    }
  }

  evtSource.onerror = () => {
    const data = { "error": "Network error" }
    onErrorChatMessage(data)
    evtSource.close()
  }

  evtSource.addEventListener("error", (event: MessageEvent) => {
    const data = { error: event.data }
    onErrorChatMessage(data)
    evtSource.close()
  })


}