import { DataTable } from "../SatelliteTable/data-table";
import Axios from "axios";
import { useEffect, useState } from "react";
import { proposedChangeURL } from "@/Constants/constants";
import { UpdateData } from "@/types/Update";
import  UpdateColumns from "./columns";

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
  }, []);

  const handleApprove:HandleChangeFunction = async (rowId: number) => {
    try {
      const response = await Axios.put(`${proposedChangeURL}/${rowId}`);
      if (response.status === 200) {
        console.log('Approved:', response.data.id);
        refreshData();
      }
    } catch (error) {
      console.error('Error approving:', error);
    }
  };
  
  const handleDeny:HandleChangeFunction = async (rowId: number) => {
    try {
      const response = await Axios.put(`${proposedChangeURL}/${rowId}`);
      console.log(`update data: ${rowId}`);
      if (response.status === 200) {
        console.log('Denied:', response.data.id);
        refreshData();
      }
    } catch (error) {
      console.error('Error denying:', error)
    }
  };

  const refreshData = async () => {
    try {
      const updateData = await Axios.get<UpdateData>(proposedChangeURL);
      setUpdate(sanitizeSatelliteDataJson(updateData.data));
    } catch (error) {
      console.error("An error occurred fetching update data. ", error);
      alert("An error occurred refreshing the data.");
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
