import { Payment, columns } from "./columns"
import { DataTable } from "./data-table"
import Axios from 'axios';
import { useEffect, useState } from 'react'
import {SatelliteData} from '../../types/Satellite';

function data(): Payment[] {
  // Fetch data from your API here.
  return [
    {
      id: "728ed52f",
      amount: 100,
      status: "pending",
      email: "m@example.com",
    },
    // ...
  ]
}

export default function DemoPage() {
  const [satellites, setSatellites] = useState<SatelliteData>({satellites: []})

  useEffect(() => {
    //setSatellites(placeholder);
     const getData = async () =>{
     try{
         const satelliteData = await Axios.get<SatelliteData>("http://localhost:8080/confirmed/satellites?limit=10");
         setSatellites(satelliteData.data);
       }
       catch(error){
         console.error("An error occurred fetching satellite data.", error);
       }
     }    
     getData();
  }, []);

  const dat = data()

  return (
    <div className="container mx-auto py-10">
      <DataTable columns={columns} data={dat} />
    </div>
  )
}
