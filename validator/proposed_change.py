from dataclasses import dataclass, field
from typing import Optional, List
from dataclasses import asdict
from utils.helpers import get_db_connection

@dataclass
class ProposedChange:
    official_name: str = ''
    reg_country: str = ''
    own_country: str = ''
    owner_name: str = ''
    user_type: str = ''
    purposes: str = ''
    orbit_class: str = ''
    orbit_type: str = ''
    geo_longitude: str = ''
    perigee: str = ''
    apogee: str = ''
    eccentricity: str = ''
    inclination: str = ''
    period_min: str = ''
    mass_launch: str = ''
    mass_dry: str = ''
    power_watts: str = ''
    launch_date: str = ''
    exp_lifetime: str = ''
    contractor: str = ''
    contractor_country: str = ''
    launch_site: str = ''
    launch_vehicle: str = ''
    cospar_number: str = ''
    norad_number: int = 0
    comment_note: str = ''
    source_orbit: str = ''
    source_satellite: List[str] = field(default_factory=list)
    scraped_website_source: str = ''
    confidence_score: float = 0
    change_id: Optional[int] = field(default=None)
    approve_denied_flag: Optional[bool] = field(default=None)
    time: Optional[str] = field(default=None)
    approved_personnel: Optional[str] = field(default=None)
    notes: Optional[str] = field(default=None)
    flagged: Optional[bool] = field(default=None)

def insert_proposed_change(proposed_change: ProposedChange, used_row_ids: List[int]):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO proposed_changes (
            official_name, reg_country, own_country, owner_name, user_type, purposes,
            orbit_class, orbit_type, geo_longitude, perigee, apogee, eccentricity,
            inclination, period_min, mass_launch, mass_dry, power_watts, launch_date,
            exp_lifetime, contractor, contractor_country, launch_site, launch_vehicle,
            cospar_number, norad_number, comment_note, source_orbit, source_satellite,
            scraped_website_source, confidence_score, approve_denied_flag, time,
            approved_personnel, notes, flagged
        )
        VALUES (
            %(official_name)s, %(reg_country)s, %(own_country)s, %(owner_name)s, %(user_type)s, %(purposes)s,
            %(orbit_class)s, %(orbit_type)s, %(geo_longitude)s, %(perigee)s, %(apogee)s, %(eccentricity)s,
            %(inclination)s, %(period_min)s, %(mass_launch)s, %(mass_dry)s, %(power_watts)s, %(launch_date)s,
            %(exp_lifetime)s, %(contractor)s, %(contractor_country)s, %(launch_site)s, %(launch_vehicle)s,
            %(cospar_number)s, %(norad_number)s, %(comment_note)s, %(source_orbit)s, %(source_satellite)s,
            %(scraped_website_source)s, %(confidence_score)s, %(approve_denied_flag)s, %(time)s,
            %(approved_personnel)s, %(notes)s, %(flagged)s
        )
    """
    cursor.execute(sql, asdict(proposed_change))
    change_id = cursor.fetchone()[0]
    conn.commit()
    
    sql = """
        UPDATE crawler_dump
        SET proposed_change_ids = array_append(proposed_change_ids, %s)
        WHERE id = ANY(%s)
    """
    cursor.execute(sql, (change_id, used_row_ids))
    conn.commit()

    cursor.close()
    conn.close()
    return change_id
