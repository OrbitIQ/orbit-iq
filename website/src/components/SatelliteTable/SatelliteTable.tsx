import { satelliteColumns } from "./columns";
import { DataTable } from "./data-table";
import Axios from "axios";
import { useEffect, useState } from "react";
import { SatelliteData } from "../../types/Satellite";
import { confirmedSatellitesURL } from "@/Constants/constants";

const sanitizeSatelliteDataJson = (data: SatelliteData): SatelliteData => {
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

export default function SatelliteTable() {
  const [satellites, setSatellites] = useState<SatelliteData>({
    satellites: [],
  });

  useEffect(() => {
    const getData = async () => {
      try {
        const satelliteData = await Axios.get<SatelliteData>(
          confirmedSatellitesURL
        );
        setSatellites(sanitizeSatelliteDataJson(satelliteData.data));
      } catch (error) {
        alert("An error occured fetching satellite data.");
        console.error("An error occurred fetching satellite data. ", error);
      }
    };
    getData();
  }, []);

  return (
    <div className="container mx-auto py-10">
      <DataTable columns={satelliteColumns} data={satellites.satellites} />
    </div>
  );
}
