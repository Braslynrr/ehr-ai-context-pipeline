import type { PatientListProp } from "../../module/patient/patient.type";
import PatientCard from "./patient.card";

export default function PatientList({ patients, onSelect, patient }: PatientListProp) {

    return (
        <div className="flex flex-col gap-1">
            {patients.map(p => {
                const isSelected = p.patient_id === patient?.patient_id

                return (
                    <PatientCard
                        key={p.patient_id}
                        patient={p}
                        selected={isSelected}
                        onSelect={() => isSelected ? onSelect(undefined) : onSelect(p)}
                    />
                )
            })}
        </div>
    )

}