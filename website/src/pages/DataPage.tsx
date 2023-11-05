import SatelliteTable from "../components/SatelliteTable/SatelliteTable";
import {Switch} from "../components/ui/switch";
import {Label} from "../components/ui/label";
import {useState} from "react";

//To add canEdit prop to the satellite table.


function DataPage() {
  const [canEdit, setCanEdit] = useState(false)

  return (
    <div className="flex flex-col items-center w-full max-w-7xl px-4 py-6 mx-auto sm:px-6 lg:px-8">
      <h1 className="text-3xl font-semibold text-gray-800 mb-4">Verified Satellite Data</h1>
      <div className="w-full overflow-x-auto">
        <SatelliteTable isEditable={canEdit} />
      </div>
      <div className="mt-4">
        <Switch id="edit-mode" onCheckedChange={() => {
            setCanEdit(!canEdit)
          }
        }/>
        <Label htmlFor="edit-mode">Edit</Label>
      </div>
    </div>
  );
}

export default DataPage;
