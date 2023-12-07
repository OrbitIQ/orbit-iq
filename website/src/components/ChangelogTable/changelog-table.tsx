import { DataTable } from "../Table/data-table";
import { changelogColumns } from "./columns";
import fetchChangeLogData from "@/requestLogic/fetchChangeLog";
import {useState} from "react";

// currently not used, but DataTable requires it
const onChangedData = () => {
}

export default function ChangelogTable() {

  const [pagination, setPagination] = useState({
    pageIndex: 1,
    pageSize: 10, //customize the default page size
  });

  return (
    <div className="container mx-auto py-10">
      <DataTable
        columns={changelogColumns}
        isEditable={false}
        // @ts-ignore
        fetchFunction={fetchChangeLogData}
        cacheKey={"change-log"}
        onChangedData={onChangedData}
        pagination={pagination}
        setPagination={setPagination}
      />
    </div>
  );
}
