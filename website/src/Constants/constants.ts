/**React Table Columns**/

//https://www.material-react-table.com/docs/guides/column-hiding

//Column Definitions
export const dataColumnDefinitions = [
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
  },
];

//Column Definitions
export const changelogColumnDefinitions = [
  {
    accessorKey: "update_user",
    header: "Update User",
  },
  {
    accessorKey: "update_action",
    header: "Update Action",
  },
  {
    accessorKey: "update_time",
    header: "Update Time",
  },
  {
    accessorKey: "update_notes",
    header: "Update Notes",
  },
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
  "apogee": false,
  "comment_note": false,
  "contractor": false,
  "contractor_country": false,
  "cospar": false,
  "detailed_purpose": false,
  "eccentricity": false,
  "exp_lifetime": false,
  "geo_longitutde": false,
  "inclination": false,
  "launch_site": false,
  "launch_vehicle": false,
  "mass_dry": false,
  "mass_launch": false,
  "orbit_type": false,
  "own_country": false,
  "perigee": false,
  "period_min": false,
  "power_watts": false,
  "purposes": false,
  "source_orbit": false,
  "source_satellite": false
}


//Params
export const paginationSize: number = 10;
export const pageSize: number = 4

//Endpoint URLs
export const confirmedSatellitesURL: string = `http://localhost:8080/confirmed/satellites`;
export const editHistoryURL: string = `http://localhost:8080/edit/history`;