import SatelliteTable from "../components/SatelliteTable/page";
import { Button } from "../components/ui/button";
import { Link } from "react-router-dom";

function DataPage() {
  return (
    <>
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
        <Link to="/updates">
          <Button variant="outline" buttonSize="icon">
            Edit
          </Button>
        </Link>
      </div>
    </>
  );
}

export default DataPage;
