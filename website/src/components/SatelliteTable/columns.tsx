import { ColumnDef } from "@tanstack/react-table"
import { Satellite } from "../../types/Satellite"
import { dataColumnDefinitions } from "@/Constants/constants";
 

export const satelliteColumns: ColumnDef<Satellite>[] = dataColumnDefinitions;