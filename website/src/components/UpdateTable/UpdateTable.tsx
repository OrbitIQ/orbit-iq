import { DataTable } from "../SatelliteTable/data-table";
import Axios from "axios";
import { useEffect, useState } from "react";
import { proposedChangeURL } from "@/Constants/constants";
import { UpdateData } from "@/types/Update";
import { UpdateColumns } from "./columns";

const sanitizeSatelliteDataJson = (data: UpdateData): UpdateData => {
  data.satellites.forEach((satellite) => {
    satellite.source_satellite = sanitizeSourceSatellite(
      satellite.source_satellite
    );

    //This needs to be fixed, guessing any of these columns can be null at any given point.
    if (satellite.mass_dry == null) satellite.mass_dry = "N/A";
    if (satellite.power_watts == null) satellite.power_watts = "N/A";
    if (satellite.source_orbit == null) satellite.power_watts = "N/A";
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

export default function UpdateTable() {
  const [update, setUpdate] = useState<UpdateData>({
    satellites: [],
  });

  useEffect(() => {
    const getData = async () => {
      try {
        const updateData = await Axios.get<UpdateData>(proposedChangeURL);
        const updateDataTest = await Axios.get<any>(proposedChangeURL);
        console.log(`update data: ${JSON.stringify(updateDataTest)}`);
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
        data={update.satellites}
        isEditable={false}
      />
    </div>
  );
}
