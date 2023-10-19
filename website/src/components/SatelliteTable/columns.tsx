import { ColumnDef } from "@tanstack/react-table"
import { Satellite } from "../../types/Satellite"


export const satelliteColumns: ColumnDef<Satellite>[] = [
  {
    accessorKey: "apogee",
    header: "Apogee",
  },
  {
    accessorKey: "comment_note",
    header: "Comment Note",
  },
  {
    accessorKey: "contractor",
    header: "Contractor",
  },
  {
    accessorKey: "contractor_country",
    header: "Contractor Country",
  },


  {
    accessorKey: "cospar",
    header: "Cospar",
  },
  {
    accessorKey: "detailed_purpose",
    header: "Detailed Purpose",
  },
  {
    accessorKey: "eccentricity",
    header: "Eccentricity",
  },
  {
    accessorKey: "exp_lifetime",
    header: "Exp Lifetime",
  },


  {
    accessorKey: "geo_longitutde",
    header: "Geo Longitude",
  },
  {
    accessorKey: "inclination",
    header: "Inclination",
  },
  {
    accessorKey: "launch_date",
    header: "Launch Date",
  },
  {
    accessorKey: "launch_site",
    header: "Launch Site",
  },


  {
    accessorKey: "launch_vehicle",
    header: "Launch Vehicle",
  },
  {
    accessorKey: "mass_dry",
    header: "Mass Dry",
  },
  {
    accessorKey: "mass_launch",
    header: "Mass Launch",
  },
  {
    accessorKey: "norad",
    header: "norad",
  },

  {
    accessorKey: "official_name",
    header: "Official Name",
  },
  {
    accessorKey: "orbit_class",
    header: "Orbit Class",
  },
  {
    accessorKey: "orbit_type",
    header: "Orbit Type",
  },
  {
    accessorKey: "own_country",
    header: "Own Country",
  },

  {
    accessorKey: "official_name",
    header: "Official Name",
  },
  {
    accessorKey: "orbit_class",
    header: "Orbit Class",
  },
  {
    accessorKey: "orbit_type",
    header: "Orbit Type",
  },
  {
    accessorKey: "own_country",
    header: "Own Country",
  },

];




// This type is used to define the shape of our data.
// You can use a Zod schema here if you want.
export type Payment = {
  id: string
  amount: number
  status: "pending" | "processing" | "success" | "failed"
  email: string
}

export const columns: ColumnDef<Payment>[] = [
  {
    accessorKey: "status",
    header: "Status",
  },
  {
    accessorKey: "email",
    header: "Email",
  },
  {
    accessorKey: "amount",
    header: "Amount",
  },
]
