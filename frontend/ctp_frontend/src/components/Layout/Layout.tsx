import Navbar from "./Navbar.tsx";
import { Outlet } from "react-router"


const Layout = () =>{
    return(
        <div className="flex min-h-screen flex-col">
            <Navbar />
            <main className="flex-1">
                <Outlet />
            </main>
        </div>
    )
}

export default Layout