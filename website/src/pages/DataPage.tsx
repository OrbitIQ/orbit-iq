import SatelliteTable from "../components/SatelliteTable/page";
import { Button } from "../components/ui/button";
import { Link } from "react-router-dom";

function DataPage() {
  return (
    <div className="flex flex-col items-center w-full max-w-7xl px-4 py-6 mx-auto sm:px-6 lg:px-8">
      <h1 className="text-3xl font-semibold text-gray-800 mb-4">Verified Satellite Data</h1>
      <div className="w-full overflow-x-auto">
        <SatelliteTable />
      </div>
      <div className="mt-4">
        <Link to="/updates">
          <Button variant="outline" buttonSize="icon" className="text-indigo-600 border-indigo-600 hover:bg-indigo-600 hover:text-white transition ease-in-out duration-150">
            Edit
          </Button>
        </Link>
      </div>
    </div>
  );
}

export default DataPage;
