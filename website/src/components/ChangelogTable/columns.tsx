import { ColumnDef } from "@tanstack/react-table"
import { changelogColumnDefinitions } from "@/Constants/constants";
import { Change } from "@/types/Change";
import { Satellite } from "@/types/Satellite"; 

export const changelogColumns: ColumnDef<Satellite|Change, unknown>[] = changelogColumnDefinitions;