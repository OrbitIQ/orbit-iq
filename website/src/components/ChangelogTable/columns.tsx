import { ColumnDef } from "@tanstack/react-table"
import { changelogColumnDefinitions } from "@/Constants/constants";
import { Change } from "@/types/Change";
 

export const changelogColumns: ColumnDef<Change>[] = changelogColumnDefinitions;