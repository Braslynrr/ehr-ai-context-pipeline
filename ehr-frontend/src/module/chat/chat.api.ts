import { apiClient } from "../../client/client";
import type { ChatRequest } from "./chat.types";


export async function getStream(data:ChatRequest): Promise<string> {
    const res = await apiClient("/ehr/ask",{method:"post", body: JSON.stringify(data)}) as string
    return res
}