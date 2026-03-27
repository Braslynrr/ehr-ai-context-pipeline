import type { PatientCardProp } from "../../module/patient/patient.type";

export default function PatientCard({ patient, selected, onSelect }: PatientCardProp) {

    return (
        <div
            onClick={onSelect}
            className={`w-full px-3 py-2 rounded-lg cursor-pointer transition-all duration-150
                ${selected
                    ? "bg-blue-600 text-white"
                    : "hover:bg-gray-800 text-gray-300"}`}>
                        
            <div className="text-sm font-medium truncate">
                {patient.name}
            </div>

            <div className="text-xs flex justify-between opacity-80">
                <span>{patient.gender}</span>
                <span>{patient.age} yrs</span>
            </div>

            <div className="text-xs opacity-70">
                Blood: {patient.blood_type}
            </div>
        </div>
    )
}