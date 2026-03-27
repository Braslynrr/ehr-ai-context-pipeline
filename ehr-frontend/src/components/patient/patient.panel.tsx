import { useEffect, useMemo, useState } from "react"
import { getPatients } from "../../module/patient/patient.api"
import type { Patient, PatientPanelProps } from "../../module/patient/patient.type"
import PatientList from "./patient.list"
import PatientFilter from "./patient.filter"

export default function PatientPanel({ onSelect, patient }: PatientPanelProps) {

    const [patients, setPatients] = useState<Patient[]>([])
    const [filterText, setFilterText] = useState<string>("");

    useEffect(() => {
        async function loadPatients() {

            const patients = await getPatients()
            setPatients(patients)
        }

        loadPatients()

    }, [])

    const filteredPatients = useMemo(() => {
        if (!filterText) return patients;

        const lower = filterText.toLowerCase();

        return patients.filter((p) =>
            Object.values(p).some((value) =>
                String(value).toLowerCase().includes(lower)
            )
        );
    }, [filterText, patients]);

    return (
        <div className="h-full w-80 bg-gray-900 text-gray-100 flex flex-col border-r border-gray-900">

            <div className="px-4 py-2 bg-blue-950">
                <h2 className="text-sm font-semibold tracking-wide text-gray-300">
                    Patients
                </h2>
            </div>

            <div className="p-3">
                <PatientFilter setFilter={setFilterText} />
            </div>

            <div className="flex-1 overflow-y-auto px-2 pb-2">
                <PatientList
                    patient={patient}
                    onSelect={onSelect}
                    patients={filteredPatients}
                />
            </div>
        </div>
    )
}