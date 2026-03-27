import type { PatientFilterProp } from "../../module/patient/patient.type";


export default function PatientFilter({ setFilter: OnChange }: PatientFilterProp) {

    return (
        <input
            className="w-full bg-gray-800 text-sm text-gray-200 placeholder-gray-400 rounded-lg px-3 py-2 outline-none focus:ring-1 focus:ring-blue-500"
            type="text"
            placeholder="Search patients..."
            onChange={(e) => OnChange(e.currentTarget.value)}
        />
    )
}