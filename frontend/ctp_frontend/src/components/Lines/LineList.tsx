import type {Line} from "./Lines.tsx";
import {useState} from "react";
import {type NavigateFunction, useNavigate} from "react-router";




const LineList = ({lines}:{lines : Line[]}) => {
    const [selected,setSelected] = useState<Line | null>(null);
    const navigate:NavigateFunction = useNavigate()

    return (
        <div>
        <div className="flex">
            <ul className="flex flex-wrap gap-2">
                {lines.map((line) => (
                    <li className="btn btn-primary" key={line.route_id} onClick={() => setSelected(line)}>{line.route_short_name}</li>
                ))}

            </ul>
        </div>
            <div className="card bg-gray-100 mt-2 rounded-md flex-wrap w-1/3 border border-gray-200">
                {selected && (
                    <div className="card p-4  items-center gap-1 inline-flex w-full"
                    onClick={()=>navigate(`/line/${selected.route_id}`)}
                    >
                        <h4 className="bg-brand text-white rounded-md p-1">{selected.route_short_name}</h4>
                        <p className="bg-gray-300 font-semibold rounded-md p-1">{selected.route_long_name}</p>

                        <button
                            className="btn btn-primary p-1.5 rounded-md ml-auto"
                            onClick={() => setSelected(null)}>X</button>
                    </div>
                )}
            </div>
        </div>

    )
}

export default LineList


