

export type Patient = {
    patient_id: string,
    name: string,
    age: 45,
    gender: string,
    blood_type: string
}

export type PatientListProp = {
    patients: Patient[]
    onSelect: React.Dispatch<React.SetStateAction<Patient|undefined>>
    patient: Patient | undefined
}

export type PatientCardProp = {
    patient: Patient
    selected?: boolean
    onSelect: () => void
}

export type PatientFilterProp = {
    setFilter: React.Dispatch<React.SetStateAction<string>>
}

export type PatientPanelProps = {
    onSelect: React.Dispatch<React.SetStateAction<Patient|undefined>>
    patient: Patient | undefined
}