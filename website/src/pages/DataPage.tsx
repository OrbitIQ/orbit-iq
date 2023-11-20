import SatelliteTable from "../components/SatelliteTable/SatelliteTable";
import { Switch } from "../components/ui/switch";
import { Label } from "../components/ui/label";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import EditModal from "@/components/SatelliteTable/EditModal";
import Axios from "axios";

function DataPage() {
  const [canEdit, setCanEdit] = useState(false)
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [updateData, setUpdateData] = useState({});

  const handleEditClick = () => {
    // Open the modal
    setIsEditModalOpen(true);
  }

  const handleEditModalCancel = () => {
    // Close the modal
    setIsEditModalOpen(false);
  };

  const handleEditModalSave = (update_user: string, update_notes: string, updateData: any) => {
    console.log('Saving edited data:', update_user, update_notes, updateData);
    // Save the edited data by calling Axios API endpoint
    updateData.forEach((rowChange: any) => {
      Axios.put(`http://localhost:8080/edit/${rowChange.official_name}`, {
        "data": rowChange,
        "update_user": update_user,
        "update_notes": update_notes,
      })
        .then(function (response) {
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

  const handleChangedData = (changedData: any) => {
    // Update the state or perform any action with the received data
    setUpdateData(changedData);
  };

  return (
    <div className="flex flex-col items-center w-full max-w-7xl px-4 py-6 mx-auto sm:px-6 lg:px-8">
      <h1 className="text-3xl font-semibold text-gray-800 mb-4">Verified Satellite Data</h1>
      <div className="w-full overflow-x-auto">
        <SatelliteTable isEditable={canEdit} handleChangedData={handleChangedData}/>
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
