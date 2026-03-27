import { NavLink } from "react-router-dom"

export default function Header({ doctor }: { doctor?: string }) {

    return (
        <header className="flex flex-row bg-blue-950 text-white py-1">
            <NavLink className="text-lg" to={"/"} >EHR Client</NavLink>
            {doctor && <button className="border border-gray-900 self-end">{doctor}</button>}
        </header>
    )

}