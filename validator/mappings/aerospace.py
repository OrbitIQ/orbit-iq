import logging
from proposed_change import ProposedChange
from utils.helpers import get_proposed_changes_columns, validate_norad, get_key, get_db_connection

def from_aerospace(record):
    data = record[3]

    # Extract and validate necessary fields
    norad = get_key(data, 'SSN')
    
    if not validate_norad(norad):
        # It's ok if we cant find norad at the moment these norads might not be in the database 
        # logging.getLogger(__name__).warning(f"Skipping record {record}: invalid NORAD ID '{norad}'")
        return None
    else:
        norad = int(norad)

    # Lets make a database query to get the official name of the satellite based on the NORAD ID
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "SELECT official_name FROM official_satellites WHERE norad = %s"
    cursor.execute(sql, (norad,))

    norad_ret = cursor.fetchone()
    name = norad_ret[0] if norad_ret else None

    cursor.close()
    conn.close()

    if not name:
        # logging.getLogger(__name__).warning(f"Skipping record {record}: NORAD ID '{norad}' not in database")
        # this is fine bc we expect some NORAD IDs to not be in the database since the database is not complete
        # and only covers satellites that are currently in orbit
        return None


    proposed_data = {
        'official_name': name,
        'norad': norad,
        'proposed_notes': f'Estimated de-orbit time {data["Aerospace Reentry Prediction (UTC)"]} (UTC)',
        'source_satellite': ["Aerospace Reentry (https://aerospace.org/reentries)"],
        'action': 'delete'
    }

    # Filter data to match columns in the database table
    columns = get_proposed_changes_columns()
    filtered_data = {key: value for key, value in proposed_data.items() if key in columns}

    return ProposedChange(**filtered_data)