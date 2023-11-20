import {
  ColumnDef,
} from "@tanstack/react-table";

export interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
  isEditable: boolean;
  // this is a function that will be called when the data changes in the table
  onChangedData: (data: TData[]) => void;
}

