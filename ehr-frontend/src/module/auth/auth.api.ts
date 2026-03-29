import { apiClient } from "../../client/client"
import type { BasicMessage } from "../message/message.type"
import type { loginRequest, meResponse } from "./auth.types"

export async function authLogin(data: loginRequest): Promise<BasicMessage> {
  const res = await apiClient("/auth/login", {method:"post", body: JSON.stringify(data)}) as BasicMessage
  return res
}

export async function authMe(): Promise<meResponse> {
  const res = await apiClient("/auth/me") as meResponse
  return res
}

export async function signOut(): Promise<BasicMessage> {
  const res = await apiClient("/auth/logout", {method:"post"}) as BasicMessage
  return res
}