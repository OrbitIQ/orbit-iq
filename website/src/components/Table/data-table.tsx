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
import PaginationControls from "./PaginationControls";
import SearchFilterDropdown from "./SearchFilterDropdown";
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


import { Button } from "@/components/ui/button";
import { useState, useEffect, useRef, useCallback, useContext } from "react";
import { columnVisibilityDefaults } from "@/Constants/constants";
import { DataTableProps } from "@/types/DataTableProps";
import reactTableCreatorFactory from "./reactTableCreatorFactory";
import { Input } from "@/components/ui/input";
import EditSlider from "./EditSlider";

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
  // onChangedData,
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

  //State for search
  const [searchActive, setSearchActive] = useState<Boolean>(false);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedColumn, setSelectedColumn] = useState<string>("official_name");


  const [updateData, setUpdateData] = useState({});



  const handleChangedData = (changedData: any) => {
    // Update the state or perform any action with the received data
    setUpdateData(changedData);
  };



  useEffect(() => {
    if(searchQuery.length===0) {
      setSearchActive(false)
    }
    else{
      setSearchActive(true);
    }
  }, [searchQuery])

  //reset pagination to defaults if there is a change to whether or not the search query is active.
  useEffect(() => {
    setPagination({
    pageIndex: 1,
    pageSize: 10, 
  });
  }, [searchActive])

  const { isLoading, error, data, isSuccess } = useQuery({
      queryKey: searchActive ? [cacheKey, searchQuery, selectedColumn, pagination.pageIndex, pagination.pageSize] : [cacheKey, pagination.pageIndex, pagination.pageSize],
      queryFn: () => searchActive ? fetchFunction(pagination.pageIndex, pagination.pageSize, searchQuery, selectedColumn) : fetchFunction(pagination.pageIndex, pagination.pageSize),
      staleTime: Infinity,
    // @ts-ignore
      keepPreviousData: false,
      cacheTime: searchActive ? 60000 : 300000 //Only cache search-query calls for 1 minute. 5-min for normal (react-query default)
    }
  );

  const [newData, setData] = useState<TData[]>(
    isSuccess ? (isProposedChanges ? data.proposed_changes : data.satellites) as TData[] : []
  );
  
  //Used for togglign edit button, NOT the same piece of state as isEditable.
  const [canEdit, setCanEdit] = useState(false)

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
    // Invoke the callback function with the updated changedData
    handleChangedData(changedData);
  }, [changedData, handleChangedData]);


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
  }

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
      <div className="flex justify-center items-center min-h-screen">
          <ProgressButton />
      </div>
    );
  }
  if(error){
    return(
      <div className="flex justify-center items-center h-screen">
        <h1 className="text-3xl font-semibold text-gray-800">An error occurred</h1>
      </div>
    
    )
  }

  return (
  <div>
    <div className="flex items-center py-4">
      <div className="flex w-full max-w-sm items-center space-x-2">
        <Input
          type="searchQuery"
          placeholder={`Enter ${selectedColumn.replace(/_/g, ' ')}...`}
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          ref={(inp) => {
            if (searchActive && inp !== null) {
              inp.focus();
            }
          }}
        />
        <SearchFilterDropdown table={table} selectedColumn={selectedColumn} setSelectedColumn={setSelectedColumn} />
      </div>

      <ColumnFilterDropdown table={table} />

      {onExportExcel !== undefined && (
        <Button onClick={onExportExcel} variant="outline" className="ml-4">
          Export to Excel
        </Button>
      )}
    </div>

    <div className="rounded-md border">
      <Table>
        <TableHeader>{renderTableHeaders(canEdit)}</TableHeader>
        <TableBody>{renderTableBodyRows(canEdit, columns)}</TableBody>
      </Table>
    </div>

    {isEditable ?
      <div className="flex items-center justify-between py-2">
        <EditSlider canEdit={canEdit} setCanEdit={setCanEdit} cacheKey={cacheKey} updateData={updateData} setUpdateData={setUpdateData}/>
        <PaginationControls handleNextPage={handleNextPage} handlePreviousPage={handlePreviousPage}/>
      </div>
      :
      <PaginationControls handleNextPage={handleNextPage} handlePreviousPage={handlePreviousPage}/>
    }
  </div>
);







}
