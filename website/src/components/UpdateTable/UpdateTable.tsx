import { DataTable } from "../Table/data-table";
import Axios from "axios";
import { useEffect, useState } from "react";
import { proposedChangeURL } from "@/Constants/constants";
import { UpdateData } from "@/types/Update";
import UpdateColumns from "./columns";
import { useSatelliteData,convertUpdateToSatellite} from '@/Context/SatelliteDataContext';
import fetchUpdateData from "@/requestLogic/fetchUpdateData";

const sanitizeSatelliteDataJson = (data: UpdateData): UpdateData => {
  data.proposed_changes.forEach((proposed_changes) => {
    proposed_changes.source_satellite = sanitizeSourceSatellite(
      proposed_changes.source_satellite
    );
    if (proposed_changes.mass_dry == null) proposed_changes.mass_dry = "N/A";
    if (proposed_changes.power_watts == null)
      proposed_changes.power_watts = "N/A";
    if (proposed_changes.source_orbit == null)
      proposed_changes.power_watts = "N/A";
  });
  return data;
};

const sanitizeSourceSatellite = (
  source_satellite: Array<null | string>
): Array<null | string> => {
  return source_satellite.filter((str) => {
    return str !== null;
  });
};


const onChangedData = () => {};

// Define the type for handleApprove and handleDeny functions
type HandleChangeFunction = (rowId: number) => Promise<void>;

export default function UpdateTable() {
  const [update, setUpdate] = useState<UpdateData>({
    proposed_changes: [],
  });
  const { addApprovedSatellite } = useSatelliteData(); // Call the hook at the top level

  useEffect(() => {
    const getData = async () => {
      try {
        const updateData = await Axios.get<UpdateData>(proposedChangeURL);
        const sanitizedData = sanitizeSatelliteDataJson(updateData.data);
        const filteredData = sanitizedData.proposed_changes.filter(item =>
          item.is_approved === "denied" || item.is_approved === "pending"
        );
        setUpdate({ proposed_changes: filteredData });
      } catch (error) {
        // alert("An error occured fetching update data.");
        console.error("An error occurred fetching update data. ", error);
      }
    };
    getData();
  }, [])

  const handleApprove: HandleChangeFunction = async (rowId: number) => {
    try {
      // Update the row to mark as 'approved' before asking for confirmation
      setUpdate(prevState => ({
        ...prevState,
        proposed_changes: prevState.proposed_changes.map(item => {
          if (item.id === rowId) {
            return { ...item, is_approved: "approved" };
          }
          return item;
        })
      }));

      if (window.confirm("Are you sure you want to approve this record?")) {
        const response = await Axios.put(`${proposedChangeURL}/approve/${rowId}`);
        if (response.status === 200) {
          console.log("Approved:", response.data.id);
         // Extract the approved satellite data
          const approvedUpdate = update.proposed_changes.find(item => item.id === rowId); 
          if (approvedUpdate) {
            const approvedSatellite = convertUpdateToSatellite(approvedUpdate);
            console.log("Converted to Satellite:", approvedSatellite);
            addApprovedSatellite(approvedSatellite);
           }
          const formData = new FormData();
          formData.append('approved_user', 'admin');
          const persistResponse = await Axios.post(`${proposedChangeURL}/persist`,
          formData);
          console.log("Response received", persistResponse);
          if (persistResponse.status === 200) {
            console.log("Persisted changes:", persistResponse.data.message);
            alert("Approval and persisting of changes confirmed.");
          }
          // Remove the row from the displayed data   
          setUpdate(prevState => ({
            ...prevState,
            proposed_changes: prevState.proposed_changes.filter(item => item.id !== rowId)
          }));
        }
      } else {
        // If not confirmed, revert the is_approved status
        setUpdate(prevState => ({
          ...prevState,
          proposed_changes: prevState.proposed_changes.map(item => {
            if (item.id === rowId) {
              return { ...item, is_approved: "pending" }; 
            }
            return item;
          })
        }));
      }
    } catch (error) {
      console.error("Error approving:", error);
      alert("An error occurred while approving or persisting changes.");
    }
  };  

  const handleDeny: HandleChangeFunction = async (rowId: number) => {
    try {
      if (window.confirm("Are you sure you want to deny this item?")) {
        const response = await Axios.put(`${proposedChangeURL}/deny/${rowId}`);
        if (response.status === 200) {
          console.log("Denied:", response.data.id);
          
          setUpdate(prevState => ({
            ...prevState,
            proposed_changes: prevState.proposed_changes.map(item => {
              if (item.id === rowId) {
                // Update the is_approved status and disable actions
                return { ...item, is_approved: "denied", actionsDisabled: true };
              }
              return item;
            })
          }));
        }
      }
    } catch (error) {
      console.error("Error denying:", error);
    }
  };
  
  const handleToggleStatus: HandleChangeFunction = async (rowId: number) => {
    try {
    const rowData = update.proposed_changes.find(item => item.id === rowId);
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
  
      const response = await Axios.put(`${proposedChangeURL}/${rowId}`, formData); 
      if (response.status === 200) {
        setUpdate(prevState => ({
          ...prevState,
          proposed_changes: prevState.proposed_changes.map(item =>
            item.id === rowData.id ? { ...item, is_approved: newStatus } : item
          )
        }));
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
        />

    </div>
  );
}
