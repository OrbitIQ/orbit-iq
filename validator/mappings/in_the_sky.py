import logging
from proposed_change import ProposedChange
from utils.helpers import get_proposed_changes_columns, validate_norad, get_key, get_db_connection
from datetime import datetime
import re

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%d %B %Y').date().isoformat()
    except ValueError:
        return None
    
def parse_float_with_suffix(value):
    return float(re.sub(r'[^\d.]+', '', value)) if value else None

def from_in_the_sky(record):
    data = record[3]

    status = get_key(data, 'Status', '').strip().lower()
    deleted_statuses = ['decayed', 'destroyed', 'failed', 'retired', 'lost', 'non-operational']
    operating_statuses = ['operational', 'partially operational']

    if str(data['norad']) != str(data['NORAD ID']):
        # uh oh
        logging.getLogger(__name__).warning(f"Skipping record {record}: NORAD ID '{data['norad']}' does not match NORAD ID '{data['NORAD ID']}'")
        return None

    if status == "unknown" or not status:
        # TODO: I am not sure if this is the right thing to do, but I am going to assume that if the status is unknown
        #      then we should not try to update or add it to the database
        return None
    
    if status in deleted_statuses:
        proposed_data = {
            'official_name': data['official_name'], # set by crawler
            'norad': data['norad'], # set by crawler
            'source_satellite': ["in-the-sky.org"],
            'action': 'delete',
            'proposed_notes': f"in-the-sky.org indicates status: {status} (https://in-the-sky.org/spacecraft.php?id={data['norad']})",
        }
    else:
        # This is an operating satellite
        proposed_data = {
            'official_name': data['official_name'], # set by crawler
            'norad': data['norad'], # set by crawler
            'launch_date': parse_date(data.get('Launched')),
            'own_country': data.get('Owner', '').strip(),
            'launch_site': data.get('Launch site', '').strip(),
            'inclination': parse_float_with_suffix(data.get('Inclination')),
            'eccentricity': parse_float_with_suffix(data.get('Eccentricity')),
            'cospar': data.get('COSPAR ID', '').strip(),
            'source_satellite': ["in-the-sky.org"],
            'action': 'update',
        }

    # Filter data to match columns in the database table
    columns = get_proposed_changes_columns()
    filtered_data = {key: value for key, value in proposed_data.items() if key in columns}

    return ProposedChange(**filtered_data)