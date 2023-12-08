"use client";

import {
  ColumnDef,
  ColumnFiltersState,
  flexRender,
  getCoreRowModel,
  getPaginationRowModel,
  VisibilityState,
} from "@tanstack/react-table";

import {useQuery} from "@tanstack/react-query";
import BottomNavBar from "./BottomNavBar";

import ProgressButton from "../ui/ProgressButton";

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

import ColumnFilterDropdown from "./ColumnFilterDropdown";

import SearchButton from "../ui/SearchButton";

import { Button } from "@/components/ui/button";
import { useState, useEffect, useRef, useCallback, } from "react";
import { columnVisibilityDefaults } from "@/Constants/constants";
import { DataTableProps } from "@/types/DataTableProps";
import reactTableCreatorFactory from "./reactTableCreatorFactory";
import { Input } from "@/components/ui/input";

const defaultColumns: Partial<ColumnDef<any>> = {
  cell: ({ getValue, row: { index }, column: { id }, table }) => {
    const initialValue = getValue()
    // We need to keep and update the state of the cell normally
    const [value, setValue] = useState(initialValue)

    // When the input is blurred, we'll call our table meta's updateData function
    const onBlur = () => {
      // @ts-ignore
      table.options.meta?.updateData(index, id, value)
    }

    // If the initialValue is changed external, sync it up with our state
    useEffect(() => {
      setValue(initialValue)
    }, [initialValue])

    return (
      <input
        value={value as string}
        onChange={e => setValue(e.target.value)}
        onBlur={onBlur}
      />
    )
  },
}

// Wrap a function with this to skip a pagination reset temporarily
function useSkipper() {
  const shouldSkipRef = useRef(true)
  const shouldSkip = shouldSkipRef.current

  const skip = useCallback(() => {
    shouldSkipRef.current = false
  }, [])

  useEffect(() => {
    shouldSkipRef.current = true
  })

  return [shouldSkip, skip] as const
}


export function DataTable<TData, TValue>({
  columns,
  isEditable,
  // @ts-ignore
  fetchFunction,
  // @ts-ignore
  cacheKey,
  onChangedData,
  // @ts-ignore
  onExportExcel,
  //Hacky, solution TODO: FIX
  // @ts-ignore
  isProposedChanges,
  // @ts-ignore
  pagination,
  // @ts-ignore
  setPagination
}: DataTableProps<TData, TValue>) {

  const [searchActive, setSearchActive] = useState<Boolean>(false);


  const { isLoading, error, data, isSuccess } = useQuery({
      queryKey: [cacheKey, pagination.pageIndex, pagination.pageSize],
      queryFn: () => fetchFunction(pagination.pageIndex, pagination.pageSize),
      staleTime: Infinity,
    // @ts-ignore
      keepPreviousData: false
    }
  );

  const [newData, setData] = useState<TData[]>(
    isSuccess ? (isProposedChanges ? data.proposed_changes : data.satellites) as TData[] : []
  );
  
  const [canEdit, setCanEdit] = useState(isEditable)
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>(
    []
  )
  const [autoResetPageIndex, skipAutoResetPageIndex] = useSkipper()



  useEffect(() => {
    // Update newData when the API call is successful
    if (isSuccess) {
      setData(isProposedChanges ? data.proposed_changes : data.satellites as TData[]);
    }
  }, [isSuccess, data]);


  // we will keep track of a list of changed data
  const [changedData, setChangedData] = useState<TData[]>([])

  useEffect(() => {
    setCanEdit(isEditable)
  }, [isEditable])


  useEffect(() => {
    // Invoke the callback function with the updated changedData
    onChangedData(changedData);
  }, [changedData, onChangedData]);


  const [columnVisibility, setColumnVisibility] = useState<VisibilityState>(
    columnVisibilityDefaults
  );

    const handlePreviousPage = () => {
    if (pagination.pageIndex > 1) {
      setPagination({
        ...pagination,
        pageIndex: pagination.pageIndex - 1,
      });
    }
  };

  const handleNextPage = () => {
    setPagination({
      ...pagination,
      pageIndex: pagination.pageIndex + 1,
    });
  };

  const table = reactTableCreatorFactory(newData, columns, getCoreRowModel, getPaginationRowModel, setColumnVisibility, columnVisibility, setData, autoResetPageIndex, skipAutoResetPageIndex, setColumnFilters, columnFilters, pagination)
  const editableTable = reactTableCreatorFactory(newData, columns, getCoreRowModel, getPaginationRowModel, setColumnVisibility, columnVisibility, setData, autoResetPageIndex, skipAutoResetPageIndex, setColumnFilters, columnFilters, pagination, defaultColumns, changedData,  setChangedData)

  const renderTableHeaders = (canEdit:boolean) => {
    const headerGroups = canEdit ? editableTable.getHeaderGroups() : table.getHeaderGroups();
    return headerGroups.map((headerGroup) => (
      <TableRow key={headerGroup.id}>
        {headerGroup.headers.map((header) => (
          <TableHead key={header.id}>
            {!header.isPlaceholder && flexRender(header.column.columnDef.header, header.getContext())}
          </TableHead>
        ))}
      </TableRow>
    ));
  };

  const renderTableBodyRows = (canEdit:boolean, columns: any) => {
    const rows = canEdit ? editableTable.getRowModel().rows : table.getRowModel().rows;
    if (rows?.length) {
      return rows.map((row) => (
        <TableRow key={row.id} data-state={row.getIsSelected() && "selected"}>
          {row.getVisibleCells().map((cell) => (
            <TableCell key={cell.id}>
              {flexRender(cell.column.columnDef.cell, cell.getContext())}
            </TableCell>
          ))}
        </TableRow>
      ));
    } else {
      return (
        <TableRow>
          <TableCell colSpan={columns.length} className="h-24 text-center">
            No results.
          </TableCell>
        </TableRow>
      );
    }
  };

  
  if (isLoading){
    return (
      <div className="container mx-auto py-10">
        <ProgressButton/>
      </div>
    );
  }
  if(error){
    return(
      <div>
        <h1>An error occured</h1>
      </div>
    )
  }
  if(onExportExcel === undefined){
    return (
      <div>
        <div className="flex items-center py-4">
          <Input
            placeholder="Filter official names..."
            value={(table.getColumn("official_name")?.getFilterValue() as string) ?? ""}
            onChange={(event) =>
              table.getColumn("official_name")?.setFilterValue(event.target.value)
            }
            className="max-w-sm"
          />

          {/* <SearchButton searchActive={searchActive} handleClick={() => {
            setSearchActive(!searchActive); 
            
          }}/> */}

          <ColumnFilterDropdown table={table}/>


        </div>

        <div className="rounded-md border">
          <Table>
            <TableHeader>
                {renderTableHeaders(canEdit)}
            </TableHeader>

            <TableBody>
              {renderTableBodyRows(canEdit, columns)}
            </TableBody>
          </Table>
        </div>

        <BottomNavBar handleNextPage={handleNextPage} handlePreviousPage={handlePreviousPage}/>

      </div>
    );
  }  
  else{
    return (
      <div>
        <div className="flex items-center py-4">
          <Input
            placeholder="Filter official names..."
            value={(table.getColumn("official_name")?.getFilterValue() as string) ?? ""}
            onChange={(event) =>
              table.getColumn("official_name")?.setFilterValue(event.target.value)
            }
            className="max-w-sm"
          />
          {/* <SearchButton searchActive={searchActive} handleClick={() => {
            setSearchActive(!searchActive); 
            setData([]);
          }}/> */}

          <ColumnFilterDropdown table={table}/>

          <Button onClick={onExportExcel} variant="outline" className="ml-4">Export to Excel</Button>
        </div>

        <div className="rounded-md border">
          <Table>
            <TableHeader>
                {renderTableHeaders(canEdit)}
            </TableHeader>

            <TableBody>
              {renderTableBodyRows(canEdit, columns)}
            </TableBody>
          </Table>
        </div>

        <BottomNavBar handleNextPage={handleNextPage} handlePreviousPage={handlePreviousPage}/>

      </div>
    );

  }

}
