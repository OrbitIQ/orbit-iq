import pytest
from app import app
from utils.helpers import get_db_connection
from datetime import datetime
import json
import logging

# This fixture will be used by the tests to send requests to the application

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_update_satellite(client):
    # Test updating a satellite
    # Actual data values
    official_name = "Aalto-1"
    reg_country = "Finland"
    own_country = "Finland"
    owner_name = "Aalto University"
    user_type = "Civil"
    purposes = "Technology Development"
    detailed_purpose = None  
    orbit_class = "LEO"
    orbit_type = "Sun-Synchronous"
    geo_longitude = 0
    perigee = 497
    apogee = 517
    eccentricity = 0.00145
    inclination = 97.45
    period_min = 94.7
    mass_launch = 5
    mass_dry = None 
    power_watts = 4.5
    launch_date = "2017/6/23"
    exp_lifetime = 2
    contractor = "Aalto University"
    contractor_country = "Finland"
    launch_site = "Satish Dhawan Space Centre"
    launch_vehicle = "PSLV"
    cospar = "2017-036L"
    norad = 42775
    comment_note = "Technology development and education."
    source_orbit = None 
    source_satellite = ["JMSatcat/10_17"]

    # Create the 'data_dict' dictionary with the actual data
    data_dict = {
        'official_name': official_name,
        'reg_country': reg_country,
        'own_country': own_country,
        'owner_name': owner_name,
        'user_type': user_type,
        'purposes': purposes,
        'detailed_purpose': detailed_purpose,
        'orbit_class': orbit_class,
        'orbit_type': orbit_type,
        'geo_longitude': geo_longitude,
        'perigee': perigee,
        'apogee': apogee,
        'eccentricity': eccentricity,
        'inclination': inclination,
        'period_min': period_min,
        'mass_launch': mass_launch,
        'mass_dry': mass_dry,
        'power_watts': power_watts,
        'launch_date': launch_date,
        'exp_lifetime': exp_lifetime,
        'contractor': contractor,
        'contractor_country': contractor_country,
        'launch_site': launch_site,
        'launch_vehicle': launch_vehicle,
        'cospar': cospar,
        'norad': norad,
        'comment_note': comment_note,
        'source_orbit': source_orbit,
        'source_satellite': source_satellite
    }

    # Create the 'body' dictionary with 'data', 'update_user', and 'update_notes'
    body = {
        'data': data_dict,
        'update_user': 'test_user',
        'update_notes': 'Test update'
    }

    response = client.put(f'/edit/{official_name}', json=body)
    assert response.status_code == 200

def test_get_all_satellites(client):
    # Test retrieving all satellites
    response = client.get('/edit/history')
    assert response.status_code == 200
    assert isinstance(response.json['satellites'], list)