import {NavLink, useNavigate} from "react-router";
import logo from "../../assets/logo.jpg";

const Navbar = () =>{
    const navigate = useNavigate()

    return(
        <>
            <div className="flex items-center text-2xl justify-between p-3 ml-20 mr-20 border-b border-b-gray-300">
                <div className="flex gap-1 items-center justify-between cursor-pointer" onClick={()=>{navigate('/')}}>
                    <img src={logo} alt="Logo CTP Cluj" className="h-24 w-34"/>
                    <h1 className="font-bold  cursor-pointer ">CTP Cluj Delays</h1>
                </div>
                <div className="flex items-center gap-2">
                    <NavLink
                        to="/"
                        className=" font-semibold text-2xl hover:text-gray-400 p-1  cursor-pointer">Home</NavLink>
                    <NavLink
                        to="/vehicles"
                        className=" font-semibold text-2xl hover:text-gray-400 p-1  cursor-pointer">Vehicles</NavLink>
                    <NavLink
                        to="/lines"
                        className="font-semibold text-2xl hover:text-gray-400 p-1 cursor-pointer">Lines</NavLink>
                    <NavLink
                        to="/about"
                        className=" font-semibold text-2xl hover:text-gray-400 p-1  cursor-pointer">About</NavLink>
                </div>
            </div>
        </>
    )
}

export default Navbar