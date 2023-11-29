import { DataTable } from "../SatelliteTable/data-table";
import Axios from "axios";
import { useEffect, useState } from "react";
import { editHistoryURL } from "@/Constants/constants";
import { ChangelogData } from "@/types/Change";
import { changelogColumns } from "./columns";

const sanitizeSatelliteDataJson = (data: ChangelogData): ChangelogData => {
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

// currently not used, but DataTable requires it
const onChangedData = () => {
}

export default function ChangelogTable() {
  const [changelog, setChangelog] = useState<ChangelogData>({
    satellites: [],
  });

  useEffect(() => {
    const getData = async () => {
      try {
        const changelogData = await Axios.get<ChangelogData>(editHistoryURL);
        const changelogDataTest = await Axios.get<any>(editHistoryURL);
        console.log(`changelog data: ${JSON.stringify(changelogDataTest)}`);
        setChangelog(sanitizeSatelliteDataJson(changelogData.data));
      } catch (error) {
        alert("An error occured fetching changelog data.");
        console.error("An error occurred fetching changelog data. ", error);
      }
    };
    getData();
  }, []);

  return (
    <div className="container mx-auto py-10">
      {/* <DataTable
        columns={changelogColumns}
        data={changelog.satellites}
        isEditable={false}
        onChangedData={onChangedData}
      /> */}
    </div>
  );
}
