import { SatelliteData } from "../types/Satellite";
import api from '@/services/AxiosInterceptor';

const sanitizeSatelliteDataJson = (data: SatelliteData): SatelliteData => {
  data.satellites.forEach((satellite) => {
    satellite.source_satellite = sanitizeSourceSatellite(
      satellite.source_satellite
    );

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

export default async function fetchSatelliteData(page: number, pageSize: number): Promise<SatelliteData>{

    const satelliteData = await api.get<SatelliteData>(
        `/confirmed/satellites?limit=${pageSize}&page=${page}`
    );

    const rel = sanitizeSatelliteDataJson(satelliteData.data).satellites;

    return {satellites: rel};

}