import { DataTable } from "../Table/data-table";

import { useState } from "react";
import UpdateColumns from "./columns";
import fetchUpdateData from "@/requestLogic/fetchUpdateData";
import { queryClientContext } from "@/context";
import {useContext} from "react";
import api from "@/services/AxiosInterceptor";

const onChangedData = () => {};


// Define the type for handleApprove and handleDeny functions
type HandleChangeFunction = (rowId: number) => Promise<void>;


export default function UpdateTable() {

  const [pagination, setPagination] = useState({
    pageIndex: 1,
    pageSize: 10, //customize the default page size
  });

  const queryContext = useContext(queryClientContext);

  const invalidateDataEntries = (dataCategory: string) => {
      queryContext?.queryClient.getQueryCache().getAll().forEach(cache =>
        {
          if(cache.queryKey[0] === dataCategory){
            queryContext?.queryClient.invalidateQueries({queryKey: cache.queryKey})
          }
        }                         
      );
  }

  const handleApprove: HandleChangeFunction = async (rowId: number) => {
    try {
      if (window.confirm("Are you sure you want to approve this record?")) {

        const response = await api.put(`/proposed/changes/approve/${rowId}`);
        if (response.status === 200) {

          const formData = new FormData();
          formData.append('approved_user', 'admin');

          const persistResponse = await api.post(`/proposed/changes/persist`,
          formData);
          console.log("Response received", persistResponse);

          if (persistResponse.status === 200) {
              //Invalidate verified data cache so that the new change will reliably show up.
              invalidateDataEntries('satellite-data');
              alert("Approval and persisting of changes confirmed.");
            }

          //Invalidate query, cause a re-fetch of the proposed-changes page. 
          invalidateDataEntries('change-log');
          queryContext?.queryClient.invalidateQueries({queryKey: ["update-log", pagination.pageIndex, pagination.pageSize]});
        }
      }     
    } catch (error) {
      console.error("Error approving:", error);
      alert("An error occurred while approving or persisting changes.");
    }
  };  

  const handleDeny: HandleChangeFunction = async (rowId: number) => {
    try {
      if (window.confirm("Are you sure you want to deny this item?")) {

        const response = await api.put(`/proposed/changes/deny/${rowId}`);
        if (response.status === 200) {
          console.log("Denied:", response.data.id);

          //Invalidate query, cause a re-fetch of the page. 
          invalidateDataEntries('change-log');
          queryContext?.queryClient.invalidateQueries({queryKey: ["update-log", pagination.pageIndex, pagination.pageSize]});
        }
      }
    } catch (error) {
      console.error("Error denying:", error);
    }
  };
  
  const handleToggleStatus: HandleChangeFunction = async (rowId: number) => {
    try {
    
    //@ts-ignore
    const rowData = queryContext?.queryClient.getQueryData(["update-log", pagination.pageIndex, pagination.pageSize]).proposed_changes.find(item => item.id === rowId);
    
    console.log(rowData);

    if (!rowData) {
      console.error("Row data not found for ID:", rowId);
      return;
    }
      //console.log("Row data:", rowData);
      const newStatus = rowData.is_approved === "denied" ? "pending" : "denied";
      const updateData = {
        ...rowData, 
        is_approved: newStatus 
      };
      const formData = new URLSearchParams();
      formData.append('data', JSON.stringify(updateData));
      formData.append('proposed_user', 'admin'); 
      formData.append('created_at', new Date().toISOString());
      formData.append('proposed_notes', 'revert changes');
  
      const response = await api.put(`/proposed/changes/${rowId}`, formData); 
      if (response.status === 200) {
        //Invalidate query, cause a re-fetch of the page. 
        queryContext?.queryClient.invalidateQueries({queryKey: ["update-log", pagination.pageIndex, pagination.pageSize]});
        invalidateDataEntries('satellite-data');
        invalidateDataEntries('change-log');
      }
    } catch (error) {
      console.error("Error changing status:", error);
      alert("An error occurred while changing the status.");
    }
  };

  return (
    <div className="container mx-auto py-10">
      <DataTable
        columns={UpdateColumns({ handleApprove, handleDeny, handleToggleStatus })}
        // @ts-ignore
        fetchFunction = {fetchUpdateData}
        cacheKey={"update-log"}
        isEditable={false}
        onChangedData={onChangedData}
        isProposedChanges={true}
        pagination={pagination}
        setPagination={setPagination}
      />
    </div>
  );
}
