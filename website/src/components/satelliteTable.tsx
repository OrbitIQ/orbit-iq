import { SatelliteData } from "../types/Satellite";
import { v4 as uuidv4 } from 'uuid';

//I'm pretty trash at react, pls don't judge me
const SatelliteTable = ({satellites}: SatelliteData) =>{
    return(
        <>
            <table width="100">
                <thead>
                    <tr>
                        <th>Apogee</th>
                        <th>Comment Note</th>
                        <th>Contractor</th>
                        <th>Contractor Country</th>
                        <th>COSPAR</th>
                        <th>Detailed Purpose</th>
                        <th>Eccentricity</th>
                        <th>Expected Lifetime</th>
                        <th>Geo Longitude</th>
                        <th>Inclination</th>
                        <th>Launch Date</th>
                        <th>Launch Site</th>
                        <th>Launch Vehicle</th>
                        <th>Mass Dry</th>
                        <th>Mass at Launch</th>
                        <th>NORAD Number</th>
                        <th>Official Name</th>
                        <th>Orbit Class</th>
                        <th>Orbit Type</th>
                        <th>Own Country</th>
                        <th>Owner Name</th>
                        <th>Perigee</th>
                        <th>Period (min)</th>
                        <th>Power Watts</th>
                        <th>Purposes</th>
                        <th>Registration Country</th>
                        <th>Source Orbit</th>
                        <th>Source Satellite</th>
                        <th>User Type</th>
                    </tr>
                </thead>
                <tbody>
                    {(satellites).map((sat) => (
                        <tr key = {uuidv4()}> 
                             <td>{sat.apogee}</td>
                            <td>{sat.comment_note}</td>
                            <td>{sat.contractor}</td>
                            <td>{sat.contractor_country}</td>
                            <td>{sat.cospar}</td>
                            <td>{sat.detailed_purpose}</td>
                            <td>{sat.eccentricity}</td>
                            <td>{sat.exp_lifetime}</td>
                            <td>{sat.geo_longitude}</td>
                            <td>{sat.inclination}</td>
                            <td>{sat.launch_date}</td>
                            <td>{sat.launch_site}</td>
                            <td>{sat.launch_vehicle}</td>
                            <td>{sat.mass_dry}</td>
                            <td>{sat.mass_launch}</td>
                            <td>{sat.norad}</td>
                            <td>{sat.official_name}</td>
                            <td>{sat.orbit_class}</td>
                            <td>{sat.orbit_type}</td>
                            <td>{sat.own_country}</td>
                            <td>{sat.owner_name}</td>
                            <td>{sat.perigee}</td>
                            <td>{sat.period_min}</td>
                            <td>{sat.power_watts}</td>
                            <td>{sat.purposes}</td>
                            <td>{sat.reg_country}</td>
                            <td>{sat.source_orbit}</td>
                            <td>{sat.source_satellite.join(', ')}</td>
                            <td>{sat.user_type}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </>
    );

}

export default SatelliteTable;