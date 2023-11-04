import "./App.css";
//import SatelliteTable from "./components/SatelliteTable/page";
//import logo from "./components/Navbar/ucslogo.webp";
//import { Button } from "./components/ui/button";
import Navbar from "./components/Navbar/Navbar";
import DataPage from "./pages/DataPage";
import UpdatesPage from "./pages/UpdatesPage";
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <div className="app-container">
      <Navbar />
      <div className="content-container">
        <Routes>
          <Route path="/" element={<DataPage />} />
          <Route path="/data" element={<DataPage />} />
          <Route path="/updates" element={<UpdatesPage />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
