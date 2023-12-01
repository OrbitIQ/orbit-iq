import { DataTable } from "../Table/data-table";
import { changelogColumns } from "./columns";
import fetchChangeLogData from "@/requestLogic/fetchChangeLog";

// currently not used, but DataTable requires it
const onChangedData = () => {
}

export default function ChangelogTable() {

  return (
    <div className="container mx-auto py-10">
      <DataTable
        columns={changelogColumns}
        isEditable={false}
        // @ts-ignore
        fetchFunction={fetchChangeLogData}
        cacheKey={"change-log"}
        onChangedData={onChangedData}
      />
    </div>
  );
}
