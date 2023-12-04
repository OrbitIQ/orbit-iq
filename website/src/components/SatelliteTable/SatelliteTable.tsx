import { satelliteColumns } from "./columns";
import { DataTable } from "../Table/data-table";
import fetchSatelliteData from "../../requestLogic/fetchSatelliteData";


export default function SatelliteTable({ isEditable, handleChangedData, cacheKey }: { isEditable: boolean; handleChangedData: any; cacheKey: any; }) {

  return (
      <div className="container mx-auto py-10">
        {/* @ts-ignore */}
        <DataTable columns={satelliteColumns} isEditable={isEditable} fetchFunction={fetchSatelliteData} onChangedData={handleChangedData} cacheKey={cacheKey}/>
      </div>
  );

}
