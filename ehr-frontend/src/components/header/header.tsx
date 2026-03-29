import { NavLink } from "react-router-dom"
import DropDown from "../dropdown/dropdown"
import { signOut } from "../../module/auth/auth.api"
import { useAuth } from "../../context/AuthContext"


export default function Header({ doctor }: { doctor?: string }) {

    const { logout, status } = useAuth()
    
    async function handleLogout(){
        try{
            await signOut()
            logout()
        }catch(err){
            console.log(err)
        }
    }

    return (
        <header className="flex flex-row justify-between bg-blue-950 text-white py-1">
            <NavLink className="text-lg px-2" to={"/"} >EHR Client</NavLink>

            
            {status==="authenticated" &&
                <div className="justify-self-end px-2">
                    <DropDown name={doctor??"unknown"}>
                        <button onClick={handleLogout} >Sign Out</button>
                    </DropDown>
                </div>
            }
        </header>
    )

}