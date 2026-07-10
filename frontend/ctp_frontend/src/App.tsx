import './App.css'
import './index.css'
import {Route, Routes} from "react-router";
import Layout from "./components/Layout/Layout.tsx";
import Home from "./components/Home.tsx";
import NotFound from "./components/Layout/NotFound.tsx";
import Lines from "./components/Lines/Lines.tsx";
import About from "./components/About.tsx";
import Vehicles from "./components/Vehicles/Vehicles.tsx";



function App() {


  return (
    <>
        <Routes>
            <Route element={<Layout/>}>
                <Route index element={<Home/>}/>
                <Route path="lines" element={<Lines/>}/>
                <Route path="lines/:lineId"/>
                <Route path="/vehicles" element={<Vehicles/>}/>
                <Route path="about" element={<About/>}/>
            </Route>
            <Route path="*" element={<NotFound/>}/>
        </Routes>


    </>
  )
}

export default App
