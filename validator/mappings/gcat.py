from proposed_change import ProposedChange
from utils.helpers import get_proposed_changes_columns

def from_gcat(record):
    data = record['data']
    
    columns = get_proposed_changes_columns()
    
    proposed_data = {
        'official_name': data.get('Name', ''),
        'reg_country': '',
        'own_country': '',
        'owner_name': data.get('Owner', ''),
        'user_type': '',
        'purposes': '',
        'orbit_class': data.get('OpOrbit', ''),
        'orbit_type': '',
        'geo_longitude': '',
        'perigee': data.get('Perigee', ''),
        'apogee': data.get('Apogee', ''),
        'eccentricity': '',
        'inclination': data.get('Inc', ''),
        'period_min': '',
        'mass_launch': data.get('TotMass', ''),
        'mass_dry': data.get('DryMass', ''),
        'power_watts': '',
        'launch_date': data.get('LDate', ''),
        'exp_lifetime': '',
        'contractor': data.get('Manufacturer', ''),
        'contractor_country': '',
        'launch_site': '',
        'launch_vehicle': '',
        'cospar_number': data.get('Satcat', ''),
        'norad_number': int(data.get('Satcat', 0)),
        'comment_note': '',
        'source_orbit': data.get('Primary', ''),
        'source_satellite': [],
        'scraped_website_source': 'GCAT',
        'confidence_score': 1.0
    }
    
    # Only keep data that matches columns in the database table
    filtered_data = {key: value for key, value in proposed_data.items() if key in columns}

    return ProposedChange(**filtered_data)
