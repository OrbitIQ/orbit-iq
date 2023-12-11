import { Button } from "@/components/ui/button"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuLabel,
  DropdownMenuRadioGroup,
  DropdownMenuRadioItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import {useState, useEffect} from "react";


export default function SearchFilterDropdown({table, selectedColumn, setSelectedColumn}: {table: any, selectedColumn: any, setSelectedColumn: any}){
    return(
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="outline">Search Criteria</Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="max-h-64 overflow-y-auto">
        <DropdownMenuLabel>Search Criteria</DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuRadioGroup value={selectedColumn} onValueChange={setSelectedColumn}>
        {table
          .getAllColumns()
          .map((column) => {
            return (
                <DropdownMenuRadioItem key={column.id} value={`${column.id}`}>{column.id}</DropdownMenuRadioItem>
            );
          })}
        </DropdownMenuRadioGroup>
      </DropdownMenuContent>
    </DropdownMenu>
    )
}