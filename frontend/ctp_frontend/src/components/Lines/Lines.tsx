import {useEffect, useState} from "react";
import LineList from "./LineList.tsx";


export interface Line{
    route_id: string;
    route_short_name: string;
    route_long_name: string;
    route_type: number;
    route_color?: string;
}

const handleError = (error:number) =>{
    throw new Error(`Network error! Status: ${error}`)
}



const Lines = () =>{
    const [lines,setLines] = useState<Line[] >([]);
    const [isLoading,setIsLoading] = useState<boolean>(true);
    const [error,setError] = useState<string>("");
    
    useEffect(()=>{
        const fetchData = async () => {
            try {
                const response = await fetch("http://localhost:8000/api/routes");
                if (!response.ok) {
                    handleError(response.status)
                }
                const result = await response.json();
                setLines(result);
            } catch (err) {
                setError(err instanceof Error ? err.message : "Unknown error");
                console.error(err)
            } finally {
                setIsLoading(false);
            }
        }

        fetchData();
    },[]);

        if(isLoading) return <div>Data is loading...</div>
        if(error) return  <div>Error {error}</div>

    return(
        <>

            <div>
                <div >
                    <h3 className="font-bold text-2xl">Lines</h3>
                    <div className="m-10">
                        {lines && <LineList lines={lines} />}
                    </div>


                </div>


            </div>
        </>
    )
}

export default Lines;