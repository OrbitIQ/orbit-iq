import "./App.css";
import Navbar from "./components/Navbar/Navbar";
import ChangelogPage from "./pages/ChangelogPage";
import DataPage from "./pages/DataPage";
import UpdatesPage from "./pages/UpdatesPage";
import { Routes, Route, Navigate } from "react-router-dom"; // Import Navigate
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import {QueryClient, QueryClientProvider} from '@tanstack/react-query';
import { SatelliteDataProvider } from '@/Context/SatelliteDataContext';


function App() {
  const queryClient = new QueryClient()

  return (
    <>
      <QueryClientProvider client={queryClient}>
        <SatelliteDataProvider> 
        <Navbar />
        <Routes>
          <Route path="/" element={<Navigate replace to="/data" />} /> {/* Redirect from "/" to "/data" */}
          <Route path="/data" element={<DataPage />} />
          <Route path="/updates" element={<UpdatesPage />} />
          <Route path="/changelog" element={<ChangelogPage />} />
        </Routes>
        <ReactQueryDevtools/>
        </SatelliteDataProvider>
      </QueryClientProvider>
    </>
  );
}

export default App;