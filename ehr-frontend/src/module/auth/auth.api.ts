import { apiClient } from "../../client/client"
import type { BasicMessage } from "../message/message.type"
import type { loginRequest } from "./auth.types"

export async function authLogin(data: loginRequest): Promise<BasicMessage> {
  const res = await apiClient("/auth/login", {method:"post", body: JSON.stringify(data)}) as BasicMessage
  return res
}