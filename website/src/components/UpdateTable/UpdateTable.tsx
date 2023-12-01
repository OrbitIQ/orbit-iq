import { DataTable } from "../Table/data-table";
import { UpdateColumns } from "./columns";
import fetchUpdateData from "@/requestLogic/fetchUpdateData";


const onChangedData = () => {};

export default function UpdateTable() {

  return (
    <div className="container mx-auto py-10">
      <DataTable
        columns={UpdateColumns}
        // @ts-ignore
        fetchFunction = {fetchUpdateData}
        cacheKey={"update-log"}
        isEditable={false}
        onChangedData={onChangedData}
      />
    </div>
  );
}
