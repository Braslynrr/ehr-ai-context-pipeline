import { useState, type JSX } from "react";


export default function DropDown({ name, children }: { name: string, children: JSX.Element }) {
    const [isOpen, setIsOpen] = useState(false);

    const toggleDropdown = () => {
        setIsOpen(!isOpen);
    };

    return <div className="elative inline-block text-left border border-gray-50 rounded-3xl r">
        <button onClick={toggleDropdown} className="px-2 cursor-pointer">{name}</button>

        {isOpen &&
            <div
                className="border border-gray-950 origin-top-right absolute right-0 mt-2 w-44 
                    rounded-md shadow-lg  ring-1 ring-black ring-opacity-5 text-center
                    focus:outline-none"
                role="menu">
                <div className="py-1" role="none">
                    {children}
                </div>

            </div>

        }

    </div>

} 