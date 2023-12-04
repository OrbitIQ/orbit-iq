import { satelliteColumns } from "./columns";
import { DataTable } from "../Table/data-table";
import {useQuery} from "@tanstack/react-query";
import fetchSatelliteData from "../../requestLogic/fetchSatelliteData";
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';
import { useSatelliteData } from '@/Context/SatelliteDataContext';


export default function SatelliteTable({ isEditable, handleChangedData }: { isEditable: boolean; handleChangedData: any }) {
  const { satellites } = useSatelliteData();

  const query = useQuery({
    queryKey: ['satellite-data',satellites ], queryFn: fetchSatelliteData})

    const combinedData = () => {
      const fetchedData = query.data?.satellites || [];
      return [...fetchedData];
    }

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

export default function SatelliteTable({ isEditable, handleChangedData, cacheKey }: { isEditable: boolean; handleChangedData: any; cacheKey: any; }) {
  return (
      <div className="container mx-auto py-10">
        {/* @ts-ignore */}
        <DataTable columns={satelliteColumns} isEditable={isEditable} fetchFunction={fetchSatelliteData} onChangedData={handleChangedData} cacheKey={cacheKey}/>
      </div>
  );

}
