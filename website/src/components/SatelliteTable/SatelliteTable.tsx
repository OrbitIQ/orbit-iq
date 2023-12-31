import { satelliteColumns } from "./columns";
import { DataTable } from "../Table/data-table";
import fetchSatelliteData from "../../requestLogic/fetchSatelliteData";
import api from "@/services/AxiosInterceptor";
import {useState} from "react";

const handleExcelExport = () => {
    api.get('/confirmed/satellites/export', {
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

export default function SatelliteTable({ cacheKey }: { cacheKey: any; }) {

  const [pagination, setPagination] = useState({
    pageIndex: 1,
    pageSize: 10, //customize the default page size
  });

  return (
      <div className="container mx-auto py-10">
        {/* @ts-ignore */}
        <DataTable columns={satelliteColumns} fetchFunction={fetchSatelliteData} cacheKey={cacheKey} onExportExcel = {handleExcelExport}
        pagination={pagination} 
        setPagination={setPagination}
        isEditable={true}
        />
      </div>
  );

}
