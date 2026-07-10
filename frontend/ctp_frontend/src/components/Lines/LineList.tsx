import type {Line} from "./Lines.tsx";
import {useState} from "react";




const LineList = ({lines}:{lines : Line[]}) => {
    const [selected,setSelected] = useState<Line | null>(null);

    return (
        <div>
        <div className="flex">
            <ul className="flex flex-wrap gap-2">
                {lines.map((line) => (
                    <li className="btn btn-primary" key={line.route_id} onClick={() => setSelected(line)}>{line.route_short_name} {selected && (
                        selected.route_long_name
                    )}</li>
                ))}

            </ul>
        </div>
            <div>
                {selected && (
                    <div className="card p-4">
                        <h4>{selected.route_short_name}</h4>
                        <p>{selected.route_long_name}</p>
                        <p>{selected.route_type}</p>
                    </div>
                )}
            </div>
        </div>

    )
}

export default LineList


