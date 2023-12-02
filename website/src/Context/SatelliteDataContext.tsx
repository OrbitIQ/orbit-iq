import React, { createContext, useState, useContext, useCallback } from 'react';
import { Satellite } from "@/types/Satellite"; 
import { Update }from "@/types/Update";

interface SatelliteDataContextType {
  satellites: Satellite[];
  setSatellites: (satellites: Satellite[]) => void;
  addApprovedSatellite: (approvedSatellite: Satellite) => void; 
}

const SatelliteDataContext = createContext<SatelliteDataContextType | undefined>(undefined);

export const useSatelliteData = () => {
  const context = useContext(SatelliteDataContext);

  if (!context) {
    throw new Error('useSatelliteData must be used within a SatelliteDataProvider');
  }
  return context;
};

interface SatelliteDataProviderProps {
  children: React.ReactNode;
}


export function convertUpdateToSatellite(update: Update): Satellite {
  return {
    apogee: update.apogee,
    comment_note: update.comment_note,
    contractor: update.contractor,
    contractor_country: update.contractor_country,
    cospar: update.cospar,
    detailed_purpose: update.detailed_purpose,
    eccentricity: update.eccentricity,
    exp_lifetime: update.exp_lifetime,
    geo_longitude: update.geo_longitude,
    inclination: update.inclination,
    launch_date: (update.launch_date instanceof Date) ? update.launch_date.toISOString() : update.launch_date,
    launch_site: update.launch_site,
    launch_vehicle: update.launch_vehicle,
    mass_dry: update.mass_dry,
    mass_launch: update.mass_launch,
    norad: update.norad,
    official_name: update.official_name,
    orbit_class: update.orbit_class,
    orbit_type: update.orbit_type,
    own_country: update.own_country,
    owner_name: update.owner_name,
    perigee: update.perigee,
    period_min: update.period_min,
    power_watts: update.power_watts,
    purposes: update.purposes,
    reg_country: update.reg_country,
    source_orbit: update.source_orbit,
    source_satellite: update.source_satellite,
    user_type: update.user_type,
  };
}


export const SatelliteDataProvider: React.FC<SatelliteDataProviderProps> = ({ children }) => {
  const [satellites, setSatellites] = useState<Satellite[]>([]);

  const addApprovedSatellite = useCallback((approvedSatellite: Satellite) => {
    console.log("Adding approved satellite:", approvedSatellite);
    console.log("Current satellites before adding:", satellites);
    setSatellites(prevSatellites => [...prevSatellites, approvedSatellite]);
  }, []);

  return (
    <SatelliteDataContext.Provider value={{ 
      satellites, 
      setSatellites,
      addApprovedSatellite 
    }}>
      {children}
    </SatelliteDataContext.Provider>
  );
};
