"use client";

import {
  ColumnDef,
  flexRender,
  getCoreRowModel,
  getPaginationRowModel,
  VisibilityState,
  useReactTable,
  Table as table,
} from "@tanstack/react-table";

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

import { useState, useEffect} from "react";
import { columnVisibilityDefaults } from "@/Constants/constants";
import { Satellite } from "@/types/Satellite";


interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
  isEditable: boolean;
}

/*
Editable column stolen from: https://codesandbox.io/p/sandbox/github/tanstack/table/tree/main/examples/react/editable-data?embed=1&file=%2Fsrc%2Fmain.tsx%3A28%2C1-52%2C2

Idea: We render the table with editable columns or non-editable columns based on the passed prop.
*/

const defaultColumns: Partial<ColumnDef<any>> = {
  cell: ({ getValue, row: { index }, column: { id }, table }) => {
    const initialValue = getValue()
    // We need to keep and update the state of the cell normally
    const [value, setValue] = useState(initialValue)

    // When the input is blurred, we'll call our table meta's updateData function
    const onBlur = () => {
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

//TODO: Add typescript types :)
// @ts-ignore
const reactTableCreatorFactory = (data, columns, getCoreRowModel, getPaginationRowModel, setColumnVisibility, columnVisibility, setData: (value: React.SetStateAction<TData[]>) => void, defaultColumns?) => {
    return useReactTable({
    data: data,
    columns: columns,
    ...defaultColumns !== undefined && {defaultColumn: defaultColumns},
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    onColumnVisibilityChange: setColumnVisibility,
    state: {
      columnVisibility,
    },
    meta: {
      updateData: (rowIndex: number, columnId: number, value: any) => {
        setData(old =>
          old.map((row, index) => {
            if (index === rowIndex) {
              return {
                ...old[rowIndex]!,
                [columnId]: value,
              }
            }
            return row
          }))
      }
    },
  });
};


export function DataTable<TData, TValue>({
  columns,
  data,
  isEditable
}: DataTableProps<TData, TValue>) {

  const [newData, setData] = useState<TData[]>(data)  
  const [canEdit, setCanEdit] = useState(isEditable)

  useEffect(() => {
    setData(data)
  }, [data])

  useEffect(() => {
    setCanEdit(isEditable)
  }, [isEditable])


  const [columnVisibility, setColumnVisibility] = useState<VisibilityState>(
    columnVisibilityDefaults
  );

  
  const table = reactTableCreatorFactory(newData, columns, getCoreRowModel, getPaginationRowModel, setColumnVisibility, columnVisibility, setData)
  const editableTable = reactTableCreatorFactory(newData, columns, getCoreRowModel, getPaginationRowModel, setColumnVisibility, columnVisibility, setData, defaultColumns)

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

  return (
    <div>
      <div className="flex items-center py-4">
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
          size="sm"
          onClick={() => {
            table.previousPage()
            editableTable.previousPage()
          }}
        >
          Previous
        </Button>
        <Button variant="outline" size="sm" onClick={() => {
            table.nextPage()
            editableTable.nextPage() 
          }}>
          Next
        </Button>
      </div>
    </div>
  );
}
