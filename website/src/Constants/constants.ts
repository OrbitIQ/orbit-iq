/**React Table Columns**/

//https://www.material-react-table.com/docs/guides/column-hiding

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