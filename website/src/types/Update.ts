export interface UpdateData {
    proposed_changes: Update[];
}

export interface Update {
    [key: string]: any;
    official_name: string;
    is_approved: string;
    reg_country: string;
    own_country: string;
    owner_name: string;
    user_type: string;
    purposes: string;
    detailed_purpose: string;
    orbit_class: string;
    orbit_type: string;
    geo_longitude: string;
    perigee: string;
    apogee: string;
    eccentricity: string;
    inclination: string;
    period_min: string;
    mass_launch: string;
    mass_dry: string;
    power_watts: string;
    launch_date: Date;
    exp_lifetime: string;
    contractor: string;
    contractor_country: string;
    launch_site: string;
    launch_vehicle: string;
    cospar: string;
    norad: number;
    comment_note: string;
    source_orbit: string;
    source_satellite: Array<null | string>;
    id: number;    
    proposed_user: string;
    proposed_notes: string;
    created_at: Date;
}