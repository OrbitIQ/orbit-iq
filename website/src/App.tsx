import "./App.css";
import SatelliteTable from "./components/SatelliteTable/page";
import logo from "./components/Sidebar/ucslogo.webp";
import { Button } from "./components/ui/button";

function App() {
  return (
    <>
      <div
        style={{
          margin: "auto",
          width: 1600,
          paddingTop: "2.3rem",
          display: "flex",
          flexDirection: "column",
          alignItems: "left",
        }}
      >
        <img src={logo} width={200} height={200} />
        <Button variant="outline" size="icon">
          Data
        </Button>
        <Button variant="outline" size="icon">
          Update
        </Button>
      </div>
      <div
        style={{
          margin: "auto",
          width: 1600,
          paddingTop: "2.3rem",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <h1>Satellite Data</h1>
        <SatelliteTable />
      </div>
    </>
  );
}

export default App;
