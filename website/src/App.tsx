import { useEffect, useState } from 'react'
import Axios from 'axios';
import placeholder from './assets/placeholderData.json'
import './App.css'
import {SatelliteData} from './types/Satellite';
import SatelliteTable from './components/satelliteTable';

function App() {

  const [satellites, setSatellites] = useState<SatelliteData>({satellites: []})

  useEffect(() => {
    setSatellites(placeholder);
    

    // const getData = async () =>{
    //   try{
    //     const satelliteData = await Axios.get<SatelliteData>("http://localhost:8080/confirmed/satellites?limit=10");
    //     setSatellites(satelliteData.data);
    //   }
    //   catch(error){
    //     console.error("An error occurred fetching satellite data.", error);
    //   }
    // }    
    // getData();
  }, []);


  return (
    <>
      <div style = {{
        margin: "auto",
        width: 800,
        paddingTop: "1rem"
      }}>
        <h1>Satellite Data</h1>
        <SatelliteTable satellites={satellites.satellites}/>

      </div>
    </>
  )
}

export default App
