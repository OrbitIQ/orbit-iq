
import { Switch } from "../ui/switch";
import { Label } from "../ui/label";
import { Button } from "@/components/ui/button";
import EditModal from "@/components/SatelliteTable/EditModal";
import { useState, useContext } from "react";
import api from "@/services/AxiosInterceptor";
import { queryClientContext } from "@/context";

export default function EditSlider({ canEdit, setCanEdit, cacheKey, updateData, setUpdateData }:
     { canEdit: boolean; setCanEdit: React.Dispatch<React.SetStateAction<boolean>>, cacheKey: any, updateData: {}, setUpdateData: React.Dispatch<React.SetStateAction<{}>>}) {
    const queryContext = useContext(queryClientContext);
    const [isEditModalOpen, setIsEditModalOpen] = useState(false);

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
        updateData.forEach((dataChange: any) => {
        api.put(`/edit/${dataChange.rowChange.official_name}`, {
            "data": dataChange.rowChange,
            "update_notes": update_notes,
        })
            .then(function (response) {
            //Invalidate prior query so we re-fetch.
            console.log(`Attempting to invalidate: ${[cacheKey, dataChange.pagination.pageIndex, dataChange.pagination.pageSize].toString()}`)
            queryContext?.queryClient.invalidateQueries({queryKey: [cacheKey, dataChange.pagination.pageIndex, dataChange.pagination.pageSize]});
            queryContext?.queryClient.getQueryCache().getAll().forEach(cache =>
                {
                if(cache.queryKey[0] === `change-log`){
                    queryContext?.queryClient.invalidateQueries({queryKey: cache.queryKey})
                }
                }                         
            );
            console.log(response);
            })
            .catch(function (error) {
            console.log(error);
            });
        });
        // TODO: add better confirmation message when data is saved.
        alert("Data saved.");
        setUpdateData([])
        // Close the modal
        setIsEditModalOpen(false);
        setCanEdit(false);
    };


    return(
        <div className="flex items-center justify-between py-2">
            <div className="flex items-center">
                <Switch id="edit-mode" checked={canEdit} onCheckedChange={() => setCanEdit(!canEdit)} />
                <Label htmlFor="edit-mode" className="ml-2">
                Edit
                </Label>
                {canEdit && (
                <>
                    <Button className="ml-2" variant={"outline"} onClick={handleEditClick}>
                    Save All
                    </Button>
                    {isEditModalOpen && (
                    <EditModal
                        onSave = {handleEditModalSave}
                        onCancel= {handleEditModalCancel}
                        isOpen = {isEditModalOpen}
                        // Pass update_user and update_notes to the modal
                        updateData = {updateData}
                    />
                    )}
                </>
                )}
            </div>
        </div>
    );

}