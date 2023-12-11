
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

    const handleEditModalSave = async (update_notes: string, updateData: any) => {
        try {
            // Use Promise.all to wait for all API calls to complete
            await Promise.all(
                updateData.map(async (dataChange: any) => {
                    // Use await to wait for the API call to complete
                    await api.put(`/edit/${dataChange.rowChange.official_name}`, {
                        "data": dataChange.rowChange,
                        "update_notes": update_notes,
                    });
                    // Invalidate prior query so we re-fetch.
                    console.log(`Attempting to invalidate: ${[cacheKey, dataChange.pagination.pageIndex, dataChange.pagination.pageSize].toString()}`);
                    queryContext?.queryClient.invalidateQueries({ queryKey: [cacheKey, dataChange.pagination.pageIndex, dataChange.pagination.pageSize] });
    
                    queryContext?.queryClient.getQueryCache().getAll().forEach(cache => {
                        if (cache.queryKey[0] === `change-log`) {
                            queryContext?.queryClient.invalidateQueries({ queryKey: cache.queryKey });
                        }
                    });
                    return Promise.resolve(); // Resolve the promise for this API call
                })
            );
    
            // If all API calls succeed, show the success alert
            alert("SUCCESS! Data saved.");
            setCanEdit(false);
        } catch (error) {
            // If any API call fails, catch the error and show an error alert, then reload the page.
            alert("ERROR! You cannot change the Official Name. Please try again.");
            window.location.reload();
            console.log(error);
        } finally {
            // Close the modal regardless of success or failure
            setUpdateData([]);
            setIsEditModalOpen(false);
        }
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