"use client";

import {
  ColumnDef,
  ColumnFiltersState,
  getFilteredRowModel,
  flexRender,
  getCoreRowModel,
  getPaginationRowModel,
  VisibilityState,
  useReactTable,
} from "@tanstack/react-table";

import {useQuery} from "@tanstack/react-query";
import fetchSatelliteData from "./fetchSatelliteData";
import CircularProgress from '@mui/material/CircularProgress';
import Box from '@mui/material/Box';
// import ErrorIcon from '@mui/icons-material/Error';

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";

import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

import { Button } from "@/components/ui/button";
import { useState, useEffect, useRef, useCallback, useReducer} from "react";
import { columnVisibilityDefaults } from "@/Constants/constants";
import { Satellite } from "@/types/Satellite";
import { DataTableProps } from "@/types/DataTableProps";

import { Input } from "@/components/ui/input";

//TODO: Have client side pagination avoid the ~2 second api call by actually using the route

/*
  Editable column stolen from: https://codesandbox.io/p/sandbox/github/tanstack/table/tree/main/examples/react/editable-data?embed=1&file=%2Fsrc%2Fmain.tsx%3A28%2C1-52%2C2
  As well as pagination-reset
*/

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


//TODO: Add typescript types :)
// @ts-ignore
const reactTableCreatorFactory = (data, columns, getCoreRowModel, getPaginationRowModel, setColumnVisibility, columnVisibility, setData: (value: React.SetStateAction<TData[]>) => void, autoResetPageIndex, skipAutoResetPageIndex, setColumnFilters, columnFilters, paginationSettings, setPagination, defaultColumns?, changedData?, setChangedData?: React.Dispatch<React.SetStateAction<TData[]>>) => {
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
      // @ts-ignore
      paginationSettings,
    },
    manualPagination: true,
    onPaginationChange: setPagination,
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

              // add rowChange to changedData, hacky way to do this but it works
              if (setChangedData !== undefined){
                setChangedData((oldData) => [...oldData, rowChange]);
              }
              
              return rowChange 
            }
            return row
          }))
      }
    },
  });
};

export function DataTable<TData, TValue>({
  columns,
  //@ts-ignore
  pagination,
  //@ts-ignore
  setPagination,
  isEditable,
  onChangedData,
}: DataTableProps<TData, TValue>) {

  //For implementation of server-side pagination.

  // const [pagination, setPagination] = useState({
  //   pageIndex: 0,
  //   pageSize: 10, //customize the default page size
  // });

  useEffect(() => {
    // Update newData when the API call is successful
    console.log(`PAGANATION CHANGED: ${pagination.pageIndex}`)
  }, [pagination]);



  const { isLoading, error, data, isSuccess } = useQuery({
      queryKey: ['satellite-data', pagination.pageIndex + 1, pagination.pageSize],
      queryFn: () => fetchSatelliteData(pagination.pageIndex + 1, pagination.pageSize),
      staleTime: Infinity,
    // @ts-ignore
      keepPreviousData: false
    }
  );

  const [newData, setData] = useState<TData[]>(isSuccess ? data.satellites as TData[] : [] )  
  const [canEdit, setCanEdit] = useState(isEditable)
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>(
    []
  )
  const [autoResetPageIndex, skipAutoResetPageIndex] = useSkipper()



  useEffect(() => {
    // Update newData when the API call is successful
    if (isSuccess) {
      setData(data.satellites as TData[]);
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

  
  const table = reactTableCreatorFactory(newData, columns, getCoreRowModel, getPaginationRowModel, setColumnVisibility, columnVisibility, setData, autoResetPageIndex, skipAutoResetPageIndex, setColumnFilters, columnFilters, pagination, setPagination)
  const editableTable = reactTableCreatorFactory(newData, columns, getCoreRowModel, getPaginationRowModel, setColumnVisibility, columnVisibility, setData, autoResetPageIndex, skipAutoResetPageIndex, setColumnFilters, columnFilters, pagination, setPagination, defaultColumns, changedData,  setChangedData)

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
       <Box
        sx={{
          display: 'flex',
          justifyContent: 'center', // Horizontally center the content
          alignItems: 'center',     // Vertically center the content
          height: '100vh',          // Make the container take the full height of the viewport
        }}
      >
          <CircularProgress />
      </Box>
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
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="ml-auto">
              Filter Columns
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="max-h-64 overflow-y-auto">
            {table
              .getAllColumns()
              .filter((column) => column.getCanHide())
              .map((column) => {
                return (
                  <DropdownMenuCheckboxItem
                    key={column.id}
                    className="capitalize"
                    checked={column.getIsVisible()}
                    onCheckedChange={(value) =>
                      column.toggleVisibility(!!value)
                    }
                  >
                    {column.id}
                  </DropdownMenuCheckboxItem>
                );
              })}
          </DropdownMenuContent>
        </DropdownMenu>
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


      <div className="flex items-center justify-end space-x-2 py-4">
        <Button
          variant="outline"
          buttonSize="sm"
          onClick={() => table.previousPage()}
        >
          Previous
        </Button>
        <Button
          variant="outline"
          buttonSize="sm"
          onClick={() => table.nextPage()}
        >
          Next
        </Button>
      </div>
    </div>
  );
}
