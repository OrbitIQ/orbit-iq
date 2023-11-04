import SatelliteTable from "../components/SatelliteTable/SatelliteTable";
import {Switch} from "../components/ui/switch";
import {Label} from "../components/ui/label";
import { useEffect, useState, cloneElement} from "react";

//To add canEdit prop to the satellite table.


function DataPage() {

  const [canEdit, setCanEdit] = useState(false)



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

        <SatelliteTable isEditable={canEdit}/>

        <div className="mb-5 flex items-center space-x-2">
          <Switch id="edit-mode" onCheckedChange={() => {
              setCanEdit(!canEdit)
            }
          }/>
          <Label htmlFor="edit-mode">Edit</Label>
        </div>        


      </div>
    </>
  );
}

export default DataPage;
