import {
  getFilteredRowModel,
  useReactTable,
} from "@tanstack/react-table";

import { Satellite } from "@/types/Satellite";


//TODO: Add typescript types :)
// @ts-ignore
export default function reactTableCreatorFactory (data, columns, getCoreRowModel, getPaginationRowModel, setColumnVisibility, columnVisibility, setData: (value: React.SetStateAction<TData[]>) => void, autoResetPageIndex, skipAutoResetPageIndex, setColumnFilters, columnFilters, pagination, defaultColumns?, changedData?, setChangedData?: React.Dispatch<React.SetStateAction<TData[]>>){ 
  return useReactTable({
  data: data,
  columns: columns,
  ...defaultColumns !== undefined && {defaultColumn: defaultColumns},
  getCoreRowModel: getCoreRowModel(),
  // getPaginationRowModel: getPaginationRowModel(),
  autoResetPageIndex,
  onColumnVisibilityChange: setColumnVisibility,
  onColumnFiltersChange: setColumnFilters,
  getFilteredRowModel: getFilteredRowModel(),

  state: {
    columnVisibility,
    columnFilters,
  },
  manualPagination: true,
  meta: {
    updateData: (rowIndex: number, columnId: number, value: any) => {
      skipAutoResetPageIndex()
      setData(old =>
        old.map((row, index) => {
          if (index === rowIndex) {
            const rowChange: Satellite = {
              ...old[rowIndex]!,
              [columnId]: value,
            }
            const dataChange = {
              rowChange: rowChange,
              pagination: pagination
            }
            // add rowChange to changedData, hacky way to do this but it works
            if (setChangedData !== undefined){
              setChangedData((oldData) => [...oldData, dataChange]);
            }
            
            return rowChange 
          }
          return row
        }))
    }
  },
});
};
