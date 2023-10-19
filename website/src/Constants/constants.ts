/**React Table Columns**/

//https://www.material-react-table.com/docs/guides/column-hiding

//Column Definitions
export const columnDefinitions = [
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
    header: "Norad",
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
    accessorKey: "owner_name",
    header: "Owner Name",
  },
  {
    accessorKey: "perigee",
    header: "Perigee",
  },
  {
    accessorKey: "period_min",
    header: "Period Min",
  },
  {
    accessorKey: "power_watts",
    header: "Power (Watts)",
  },
  {
    accessorKey: "purposes",
    header: "Purposes",
  },
  {
    accessorKey: "reg_country",
    header: "Registered Country",
  },
  {
    accessorKey: "source_orbit",
    header: "Source Orbit",
  },
  {
    accessorKey: "source_satellite",
    header: "Source Satellite",
  },
  {
    accessorKey: "user_type",
    header: "User Type",
  }
];

//Default visible columns 😈 
export const columnVisibilityDefaults= {
    source_orbit: false,
    purposes: false,
    power_watts: false,
    period_min: false,
    perigee: false,
    mass_launch: false,
    mass_dry: false
}


//Params
export const paginationSize: number = 10;

//Endpoint URLs
export const confirmedSatellitesURL: string = `http://localhost:8080/confirmed/satellites?limit=${paginationSize}`;