import { DataTable } from "../SatelliteTable/data-table";
import Axios from "axios";
import { useEffect, useState } from "react";
import { proposedChangeURL } from "@/Constants/constants";
import { UpdateData } from "@/types/Update";
import { UpdateColumns } from "./columns";

const sanitizeSatelliteDataJson = (data: UpdateData): UpdateData => {
  console.log(data.proposed_changes);
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

export default function UpdateTable() {
  const [update, setUpdate] = useState<UpdateData>({
    proposed_changes: [],
  });

  useEffect(() => {
    const getData = async () => {
      try {
        const updateData = await Axios.get<UpdateData>(proposedChangeURL);
        const updateDataTest = await Axios.get<any>(proposedChangeURL);
        console.log(`update data: ${JSON.stringify(updateDataTest)}`);
        console.log(`update data: ${JSON.stringify(updateData)}`);
        sanitizeSatelliteDataJson(updateData.data);
        setUpdate(sanitizeSatelliteDataJson(updateData.data));
      } catch (error) {
        alert("An error occured fetching update data.");
        console.error("An error occurred fetching update data. ", error);
      }
    };
    getData();
  }, []);

  return (
    <div className="container mx-auto py-10">
      <DataTable
        columns={UpdateColumns}
        data={update.proposed_changes}
        isEditable={false}
        onChangedData={onChangedData}
      />
    </div>
  );
}
