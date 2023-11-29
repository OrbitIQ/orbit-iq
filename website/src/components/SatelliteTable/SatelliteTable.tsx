import { satelliteColumns } from "./columns";
import { DataTable } from "./data-table";
import {useState} from "react";
import {useQuery} from "@tanstack/react-query";
import fetchSatelliteData from "./fetchSatelliteData";
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';



export default function SatelliteTable({ isEditable, handleChangedData }: { isEditable: boolean; handleChangedData: any }) {
  // const query = useQuery({ queryKey: ['satellite-data'], queryFn: fetchSatelliteData})

  // if(query.isLoading){
  //   return (
  //     <div className="container mx-auto py-10">
  //      <Box
  //       sx={{
  //         display: 'flex',
  //         justifyContent: 'center', // Horizontally center the content
  //         alignItems: 'center',     // Vertically center the content
  //         height: '100vh',          // Make the container take the full height of the viewport
  //       }}
  //     >
  //         <CircularProgress />
  //     </Box>
  //     </div>
  //   );
  // }
  // if(query.error){
  //   alert("Failed to fetch query results")
  //   return(
  //     <>
  //     </>
  //   );
  // }

  const [pagination, setPagination] = useState({
    pageIndex: 0,
    pageSize: 10, //customize the default page size
  });

  return (
      <div className="container mx-auto py-10">
        {/* @ts-ignore */}
        <DataTable columns={satelliteColumns} pagination={pagination} setPagination={setPagination} isEditable={isEditable} onChangedData={handleChangedData}/>
      </div>
  );

}
