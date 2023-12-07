import SatelliteTable from "../components/SatelliteTable/SatelliteTable";
import {useContext, useEffect} from "react";
import { Switch } from "../components/ui/switch";
import { Label } from "../components/ui/label";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import EditModal from "@/components/SatelliteTable/EditModal";
import { queryClientContext } from "@/context";
import api from "@/services/AxiosInterceptor";
import AuthService from "@/services/AuthService";

function DataPage() {
  const cacheKey = "satellite-data"
  const [canEdit, setCanEdit] = useState(false)
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [updateData, setUpdateData] = useState({});

  const queryContext = useContext(queryClientContext);

  const handleEditClick = () => {
    // Open the modal
    setIsEditModalOpen(true);
  }

  const handleEditModalCancel = () => {
    // Close the modal
    setIsEditModalOpen(false);
  };

  const handleEditModalSave = (update_notes: string, updateData: any) => {
    // Save the edited data by calling Axios API endpoint
    //TODO: Update this to a mutator.
    updateData.forEach((dataChange: any) => {
      api.put(`/edit/${dataChange.rowChange.official_name}`, {
        "data": dataChange.rowChange,
        "update_notes": update_notes,
      })
        .then(function (response) {
          //Invalidate prior query so we re-fetch.
          console.log(`Attempting to invalidate: ${[cacheKey, dataChange.pagination.pageIndex, dataChange.pagination.pageSize].toString()}`)
          queryContext?.queryClient.invalidateQueries({queryKey: [cacheKey, dataChange.pagination.pageIndex, dataChange.pagination.pageSize]});
          console.log(response);
        })
        .catch(function (error) {
          console.log(error);
        });
    });
    // TODO: add better confirmation message when data is saved.
    alert("Data saved.");
    // Close the modal
    setIsEditModalOpen(false);
    setCanEdit(false);
  };

  const handleExcelExport = () => {
    api.get('/confirmed/satellites/export', {
      responseType: 'blob', // important
    }).then((response) => {
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

  const handleChangedData = (changedData: any) => {
    // Update the state or perform any action with the received data
    setUpdateData(changedData);
  };
  
  return (
    <div className="flex flex-col items-center w-full max-w-7xl px-4 py-6 mx-auto sm:px-6 lg:px-8">
      <h1 className="text-3xl font-semibold text-gray-800 mb-4">
        Verified Satellite Data
      </h1>
      <Button onClick={handleExcelExport}>Export to Excel</Button>
      <div className="w-full overflow-x-auto">
        <SatelliteTable isEditable={canEdit} handleChangedData={handleChangedData} cacheKey = {cacheKey}/>
      </div>
      <div className="flex items-center mt-4">
        {/* Wrap Switch and Label in a flex container to align them vertically */}
        <div className="flex items-center">
          <Switch id="edit-mode" checked={canEdit} onCheckedChange={() => setCanEdit(!canEdit)} />
          <Label htmlFor="edit-mode" className="ml-2">Edit</Label> {/* Add margin-left to Label for spacing */}
      </div>
      </div>
      <div className="flex items-center mt-4">
        {canEdit && (
        <div>
          <Button onClick={handleEditClick} >Save All</Button>
          {isEditModalOpen && (
            <EditModal
              onSave={handleEditModalSave}
              onCancel={handleEditModalCancel}
              isOpen={isEditModalOpen}
              // Pass update_user and update_notes to the modal
              updateData={updateData}
            />
          )}
        </div>
      )}
      </div>
    </div>
  );
}

export default DataPage;
