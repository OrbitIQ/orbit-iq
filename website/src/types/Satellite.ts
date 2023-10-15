export interface SatelliteData {
    satellites: Satellite[];
}

export interface Satellite {
    apogee:             string;
    comment_note:       string;
    contractor:         string;
    contractor_country: string;
    cospar:             string;
    detailed_purpose:   string;
    eccentricity:       string;
    exp_lifetime:       string;
    geo_longitude:      string;
    inclination:        string;
    launch_date:        string;
    launch_site:        string;
    launch_vehicle:     string;
    mass_dry:           null;
    mass_launch:        string;
    norad:              number;
    official_name:      string;
    orbit_class:        string;
    orbit_type:         string;
    own_country:        string;
    owner_name:         string;
    perigee:            string;
    period_min:         string;
    power_watts:        null;
    purposes:           string;
    reg_country:        string;
    source_orbit:       null;
    source_satellite:   Array<null | string>;
    user_type:          string;
}