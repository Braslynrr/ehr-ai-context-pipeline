const BASE_URL = import.meta.env.VITE_EHR_API_URL

type ApiOptions = RequestInit & {
  params?: Record<string, string>
}

export async function apiClient<T>(
  endpoint: string,
  options: ApiOptions = {}
): Promise<T> {
  let url = `${BASE_URL}${endpoint}`

  console.log(BASE_URL)

  if (options.params) {
    const query = new URLSearchParams(options.params).toString()
    url += `?${query}`
  }

  const response = await fetch(url, {
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  })

  if (!response.ok) {
    const text = await response.text()
    throw new Error(text || "Request failed")
  }

  if (response.status === 204) {
    return {} as T
  }

  return response.json()
}