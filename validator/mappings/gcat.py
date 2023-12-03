import logging
from proposed_change import ProposedChange
from utils.helpers import get_proposed_changes_columns, validate_norad, get_key
from datetime import datetime

def from_gcat(record):
    data = record[3]

    # Skip debris records
    name = get_key(data, 'Name', '')
    name = name.strip()
    if name.lower().startswith("deb "):
        return None

    # Extract and validate necessary fields
    norad = get_key(data, 'Satcat')
    # Check for required fields (NORAD, Name)
    # if any field are missing or '' then report error and skip record, otherwise continue
    if not norad or not name:
        # if everything on data is None then don't log anything, it's ok if #JCAT has a non none value
        all_none = True
        for key, value in data.items():
            if key != '#JCAT' and value is not None:
                all_none = False
                break 

        if not all_none:
            logging.getLogger(__name__).warning(f"Skipping record {record}: missing required fields got NORAD ID '{norad}', and Name '{name}'")
        return None
    
    if not validate_norad(norad):
        logging.getLogger(__name__).warning(f"Skipping record {record}: invalid NORAD ID '{norad}'")
        return None
    else:
        norad = int(norad)

    # Extract other fields based on the column names
    # TODO: Should validate these assumptions
    # TODO: We need and should find out what the State column really is and what it applies to
    # TODO: Maybe we should join State/Owner/Manufacturer against https://planet4589.org/space/gcat/web/orgs/index.html
    #       to get the full name of the country/owner/manufacturer

    # alt names
    alt_names = []
    vals = get_key(data, 'AltNames', '').split(',')
    if vals is not None:
        for val in vals:
            if val.strip() != '':
                alt_names.append(val.strip())

    pl_name = get_key(data, 'PLName', '').strip()
    if pl_name != '' and pl_name not in alt_names and pl_name != name:
        alt_names.append(pl_name)

    status = get_key(data, 'Status', '').strip()
    if status != "O":
        # Status O designates in orbit, so if it's not O then it's not in orbit so we don't want it
        return None
        
    # source should be in format: JMSatcat/3_23 where 3_23 is month and year
    # need to generate it
    source = datetime.now().strftime("JMSatcat/%m_%y")


    proposed_data = {
        'official_name': name,
        'reg_country': get_key(data, 'State', '').strip(),
        'own_country': get_key(data, 'State', '').strip(),
        'owner_name': get_key(data, 'Owner', '').strip(),
        'user_type': get_key(data, 'Type', '').strip(),
        # 'purposes': '',  # Not provided in the table
        'orbit_class': get_key(data, 'OpOrbit', '').strip(),
        'orbit_type': get_key(data, 'OQUAL', '').strip(),  # Orbital quality/characteristic
        # 'geo_longitude': '',  # Not provided in the table
        'perigee': get_key(data, 'Perigee', None),
        'apogee': get_key(data, 'Apogee', '').strip(),
        # 'eccentricity': '',  # Not provided in the table
        'inclination': get_key(data, 'Inc', None),
        # 'period_min': '',  # Not provided in the table
        'mass_launch': get_key(data, 'TotMass', None),
        'mass_dry': get_key(data, 'DryMass', None),
        # 'power_watts': '',  # Not provided in the table
        'launch_date': get_key(data, 'LDate', None),
        # 'exp_lifetime': '',  # Not provided in the table
        'contractor': get_key(data, 'Manufacturer', '').strip(),
        'contractor_country': get_key(data, 'State', '').strip(),
        # 'launch_site': '',  # Not provided in the table
        # 'launch_vehicle': '',  # Not provided in the table
        'cospar': get_key(data, 'Piece', '').strip(),
        'norad': norad,
        # 'comment_note': '',  # Not provided in the table
        'source_orbit': get_key(data, 'Primary', '').strip(),
        'source_satellite': [source], # TODO: not sure this is same as source, we should sort of make sure the columns of official_satellite are 1:1 with UCS's satellite table
        'confidence_score': 1.0,  # Default value
        'alternative_names': alt_names
    }


    # Filter data to match columns in the database table
    columns = get_proposed_changes_columns()
    filtered_data = {key: value for key, value in proposed_data.items() if key in columns}

    return ProposedChange(**filtered_data)