import { satelliteColumns } from "./columns";
import { DataTable } from "./data-table";
import {useQuery} from "@tanstack/react-query";
import fetchSatelliteData from "./fetchSatelliteData";
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';
import { useSatelliteData } from '@/Context/SatelliteDataContext';
import { useEffect, useRef} from "react"


export default function SatelliteTable({ isEditable, handleChangedData }: { isEditable: boolean; handleChangedData: any }) {
  const { satellites } = useSatelliteData();
  const prevSatellitesRef = useRef(satellites);

  const query = useQuery({
    queryKey: ['satellite-data',satellites ], queryFn: fetchSatelliteData})

    const combinedData = () => {
      const fetchedData = query.data?.satellites || [];
      return [...satellites, ...fetchedData];
    }

  useEffect(() => {
    console.log("Type of satellites:", typeof satellites, "Value:", satellites);

    // Proceed only if satellites is an array
    if (Array.isArray(satellites)) {
      const newSatellites = satellites.filter(satellite => !prevSatellitesRef.current.includes(satellite));
    
      if (newSatellites.length > 0) {
        console.log("New Satellites in SatelliteTable:", newSatellites);
      }else{
        console.log("debug for newSatellites", newSatellites);
      }

      prevSatellitesRef.current = satellites;
    }
  }, [satellites]);

  
  if(query.isLoading){
    return (
      <div className="container mx-auto py-10">
       <Box
        sx={{
          display: 'flex',
          justifyContent: 'center', // Horizontally center the content
          alignItems: 'center',     // Vertically center the content
          height: '100vh',          // Make the container take the full height of the viewport
        }}
      >
          <CircularProgress />
      </Box>
      </div>
    );
  }
  if(query.error){
    alert("Failed to fetch query results")
    return(
      <>
      </>
    );
  }
  return (
      <div className="container mx-auto py-10">
        <DataTable columns={satelliteColumns} data={combinedData()} isEditable={isEditable} onChangedData={handleChangedData}/>
      </div>
  );

}
