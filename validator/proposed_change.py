from dataclasses import dataclass, field
from typing import Optional, List
from dataclasses import asdict
from utils.helpers import get_db_connection
import logging

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
    cospar: str = ''
    norad: int = 0
    comment_note: str = ''
    source_orbit: str = ''
    proposed_user: str = field(default='web crawler')
    source_satellite: List[str] = field(default_factory=list) # TODO: This might supposed to be the source satellite that launched the satellite like bus? idk we gotta check
    confidence_score: float = 0
    change_id: Optional[int] = field(default=None)
    is_approved: Optional[str] = field(default='pending')
    proposed_notes: Optional[str] = field(default=None)
    flagged: Optional[bool] = field(default=None)
    alternative_names: Optional[List[str]] = field(default_factory=list)
    action: Optional[str] = field(default='update') # can be 'update' or 'delete' at the moment

def insert_proposed_change(proposed_change: ProposedChange, used_row_ids: List[int]):
    # TODO: We probably only want to update the satellite if there are changes
    # from what's currently in the database on official_satellites
    conn = get_db_connection()
    cursor = conn.cursor()

     # Fetch current data from official_satellites
    cursor.execute("SELECT * FROM official_satellites WHERE official_name = %s", (proposed_change.official_name,))
    current_data = cursor.fetchone()

    # Compare current data with proposed_change
    is_different = False
    if current_data is not None:
        # Convert current_data (tuple) to a dictionary for easy comparison
        columns = [desc[0] for desc in cursor.description]
        current_data_dict = dict(zip(columns, current_data))

        for field in asdict(proposed_change):
            if field in current_data_dict and getattr(proposed_change, field) != current_data_dict[field]:
                is_different = True
                break
    else:
        # If there is no current data, it means this is a new entry
        is_different = True

    if not is_different:
        logging.getLogger().info(f"Proposed change for {proposed_change.official_name} is the same as current data. Skipping...")
        return None

    sql = """
        INSERT INTO proposed_changes (
            official_name, reg_country, own_country, owner_name, user_type, purposes,
            orbit_class, orbit_type, geo_longitude, perigee, apogee, eccentricity,
            inclination, period_min, mass_launch, mass_dry, power_watts, launch_date,
            exp_lifetime, contractor, contractor_country, launch_site, launch_vehicle,
            cospar, norad, comment_note, source_orbit, source_satellite, confidence_score,
            is_approved, proposed_notes, flagged, proposed_user, alternative_names, action
        )
        VALUES (
            %(official_name)s, %(reg_country)s, %(own_country)s, %(owner_name)s, %(user_type)s, %(purposes)s,
            %(orbit_class)s, %(orbit_type)s, %(geo_longitude)s, %(perigee)s, %(apogee)s, %(eccentricity)s,
            %(inclination)s, %(period_min)s, %(mass_launch)s, %(mass_dry)s, %(power_watts)s, %(launch_date)s,
            %(exp_lifetime)s, %(contractor)s, %(contractor_country)s, %(launch_site)s, %(launch_vehicle)s,
            %(cospar)s, %(norad)s, %(comment_note)s, %(source_orbit)s, %(source_satellite)s,
            %(confidence_score)s, %(is_approved)s, %(proposed_notes)s, %(flagged)s, %(proposed_user)s, %(alternative_names)s, %(action)s
        )
        RETURNING id
    """

    # Set created_at to be current
    proposed_change.created_at = 'now()'

    for field_name in ['launch_date']:  # Add any other date fields here
        if getattr(proposed_change, field_name) == '':
            setattr(proposed_change, field_name, None)

    cursor.execute(sql, asdict(proposed_change))
    change_id = cursor.fetchone()[0]
    conn.commit()

    # Insert associations into crawler_dump_proposed_changes
    sql = """
        INSERT INTO crawler_dump_proposed_changes (crawler_dump_id, proposed_change_id)
        VALUES (%s, %s)
    """
    for row_id in used_row_ids:
        cursor.execute(sql, (row_id, change_id))
    conn.commit()

    cursor.close()
    conn.close()
    return change_id

