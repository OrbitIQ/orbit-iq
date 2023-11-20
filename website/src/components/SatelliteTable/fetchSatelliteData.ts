import Axios from 'axios';
import { SatelliteData } from "../../types/Satellite";
import { confirmedSatellitesURL } from "@/Constants/constants";

//TODO: Add pagination support here.
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

export default async function fetchSatelliteData(): Promise<SatelliteData>{
    const satelliteData = await Axios.get<SatelliteData>(
        confirmedSatellitesURL
    );

    const rel = sanitizeSatelliteDataJson(satelliteData.data).satellites;

    return {satellites: rel};

}