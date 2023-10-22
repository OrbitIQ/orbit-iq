import "./App.css";
//import SatelliteTable from "./components/SatelliteTable/page";
//import logo from "./components/Navbar/ucslogo.webp";
//import { Button } from "./components/ui/button";
import Navbar from "./components/Navbar/Navbar"
import DataPage from "./components/DataPage/DataPage";
import UpdatesPage from "./components/UpdatesPage/UpdatesPage";
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <>
      <Navbar />

      <Routes>
        <Route path="/" element={<DataPage />} />
        <Route path="/data" element={<DataPage />} />
        <Route path="/updates" element={<UpdatesPage />} />
      </Routes>
    </>
  );

}

export default App;
