import "./App.css";
//import SatelliteTable from "./components/SatelliteTable/page";
//import logo from "./components/Navbar/ucslogo.webp";
//import { Button } from "./components/ui/button";
import Navbar from "./components/Navbar/Navbar";
import ChangelogPage from "./pages/ChangelogPage";
import DataPage from "./pages/DataPage";
import UpdatesPage from "./pages/UpdatesPage";
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<DataPage />} />
        <Route path="/data" element={<DataPage />} />
        <Route path="/updates" element={<UpdatesPage />} />
        <Route path="/changelog" element={<ChangelogPage />} />
      </Routes>
    </>
  );
}

export default App;
