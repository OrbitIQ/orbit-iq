import { satelliteColumns } from "./columns";
import { DataTable } from "../Table/data-table";
import fetchSatelliteData from "../../requestLogic/fetchSatelliteData";
import Axios from "axios";
import {useState} from "react";

const handleExcelExport = () => {
    Axios.get('http://localhost:8080/confirmed/satellites/export', {
      responseType: 'blob', // important
    }).then((response: any) => {
      // create file link in browser's memory
      const href = URL.createObjectURL(response.data);
  
      // create "a" HTML element with href to file & click
      const link = document.createElement('a');
      link.href = href;
      link.setAttribute('download', 'data.csv'); //or any other extension
      document.body.appendChild(link);
      link.click();
  
      // clean up "a" element & remove ObjectURL
      document.body.removeChild(link);
      URL.revokeObjectURL(href);
    });
}

export default function SatelliteTable({ isEditable, handleChangedData, cacheKey }: { isEditable: boolean; handleChangedData: any; cacheKey: any; }) {

  const [pagination, setPagination] = useState({
    pageIndex: 1,
    pageSize: 10, //customize the default page size
  });

  return (
      <div className="container mx-auto py-10">
        {/* @ts-ignore */}
        <DataTable columns={satelliteColumns} isEditable={isEditable} fetchFunction={fetchSatelliteData} onChangedData={handleChangedData} cacheKey={cacheKey} onExportExcel = {handleExcelExport}
        pagination={pagination} 
        setPagination={setPagination}
        />
      </div>
  );

}
