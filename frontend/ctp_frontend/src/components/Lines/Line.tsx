import {MapContainer, TileLayer} from "react-leaflet";
import "leaflet/dist/leaflet.css"

const position : [number,number] = [46.770439,23.591423]

const Line = () =>{
    return(
        <div className="block">
            <div>
                <div className="block items-center w-1/2 m-10 shadow-sm rounded-md p-4">
                    <h3 className="font-bold text-2xl">Line details</h3>
                    <p>Line</p>
                </div>
            </div>

        <div className="block items-center justify-center w-1/2 m-10">
            <MapContainer center={position} zoom={13}>
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />

            </MapContainer>
        </div>
        </div>
    )
}

export default Line