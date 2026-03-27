import { apiClient } from "../../client/client";
import type { Patient } from "./patient.type";

export async function getPatients(): Promise<Patient[]> {
  const res = await apiClient("/ehr/patients") as Patient[]
  return res
}