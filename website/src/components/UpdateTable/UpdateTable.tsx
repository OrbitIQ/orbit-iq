import { DataTable } from "../SatelliteTable/data-table";
import Axios from "axios";
import { useEffect, useState } from "react";
import { proposedChangeURL } from "@/Constants/constants";
import { UpdateData } from "@/types/Update";
import UpdateColumns from "./columns";
import { useSatelliteData } from '@/Context/SatelliteDataContext';

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

  useEffect(() => {
    const getData = async () => {
      try {
        const updateData = await Axios.get<UpdateData>(proposedChangeURL);
        //const updateDataTest = await Axios.get<any>(proposedChangeURL);
        //console.log(`update data test: ${JSON.stringify(updateDataTest)}`);
        console.log(`update data: ${JSON.stringify(updateData)}`);
        sanitizeSatelliteDataJson(updateData.data);
        setUpdate(sanitizeSatelliteDataJson(updateData.data));
        //console.log('Approved id:', JSON.stringify(updateData.data.id));
      } catch (error) {
        alert("An error occured fetching update data.");
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
          const approvedSatellite = update.proposed_changes.find(item => item.id === rowId); 
          const { addApprovedSatellite } = useSatelliteData();
          if (approvedSatellite) {
            addApprovedSatellite(approvedSatellite);
           }
          // Remove the row from the displayed data   
          setUpdate(prevState => ({
            ...prevState,
            proposed_changes: prevState.proposed_changes.filter(item => item.id !== rowId)
          }));
  
          // Alert the user about successful approval
          alert("Approval confirmed! The row has been moved to the verified data page.");
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
  

  return (
    <div className="container mx-auto py-10">
      <DataTable
        columns={UpdateColumns({ handleApprove, handleDeny })}
        data={update.proposed_changes}
        isEditable={false}
        onChangedData={onChangedData}
      />
    </div>
  );
}
