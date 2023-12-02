import React, { createContext, useState, useContext, useCallback } from 'react';
import { Satellite } from "@/types/Satellite"; 
import { Update }from "@/types/Satellite";
import axios from 'axios';
import { proposedChangeURL } from "@/Constants/constants";

interface SatelliteDataContextType {
  satellites: (Satellite| Update)[];
  setSatellites: (satellites: (Satellite|Update)[]) => void;
  addApprovedSatellite: (approvedSatellite: Satellite|Update) => void; // New function to add approved satellite
  fetchSatellites: (id?: number) => void; 
  shouldRefetch: boolean;
  setShouldRefetch: (value: boolean) => void;
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

export const SatelliteDataProvider: React.FC<SatelliteDataProviderProps> = ({ children }) => {
  const [satellites, setSatellites] = useState<Satellite[]>([]);
  const [shouldRefetch, setShouldRefetch] = useState(false);

  const fetchSatellites = useCallback(async (id?: number) => {
    try {
      const url = id ? `${proposedChangeURL}/changes/${id}` : `${proposedChangeURL}/changes`;
      const response = await axios.get(url);
      setSatellites(response.data);
    } catch (error) {
      console.error('Error fetching satellites:', error);
    }
  }, []);

  // Function to add an approved satellite to the satellites array
  const addApprovedSatellite = useCallback((approvedSatellite: Satellite) => {
    setSatellites(prevSatellites => [...prevSatellites, approvedSatellite]);
  }, []);

  return (
    <SatelliteDataContext.Provider value={{ satellites, setSatellites, addApprovedSatellite, fetchSatellites, shouldRefetch, setShouldRefetch }}>
      {children}
    </SatelliteDataContext.Provider>
  );
};
