import pytest
from app import app
from utils.helpers import get_db_connection
from datetime import datetime
import json

from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_jwt_required():
    with patch('flask_jwt_extended.jwt_required', lambda fn: fn):
        yield

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_create_proposed_change(client):
    # Define a sample data payload
    data = {
        'data': json.dumps({
            'official_name': 'New Satellite',
            'reg_country': 'USA',
            'own_country': 'USA',
            'owner_name': 'Owner Name',
            'user_type': 'User Type',
            'purposes': 'Purposes',
            'detailed_purpose': 'Detailed Purpose',
            'orbit_class': 'Orbit Class',
            'orbit_type': 'Orbit Type',
            'geo_longitude': 0,
            'perigee': 497,
            'apogee': 517,
            'eccentricity': 0.00145,
            'inclination': 97.45,
            'period_min': 94.7,
            'mass_launch': 5,
            'mass_dry': 50,
            'power_watts': 4.5,
            'launch_date': '2023-10-29',
            'exp_lifetime': 2,
            'contractor': 'Contractor',
            'contractor_country': 'Contractor Country',
            'launch_site': 'Launch Site',
            'launch_vehicle': 'Launch Vehicle',
            'cospar': "2017-036L",
            'norad': 42775,
            'comment_note': 'Comment Note',
            'source_orbit': 'Source Orbit',
            'source_satellite': ['Source Satellite']
        }),
        'proposed_user': 'Test User',
        'created_at': '2023-10-29',
        'proposed_notes': 'Test Notes',
    }

    response = client.post('/proposed/changes', data=data)

    assert response.status_code == 201  # Check for a successful creation

def test_get_proposed(client):
    response = client.get('/proposed/changes')
    assert response.status_code == 200  # Check for a successful retrieval
    # Add more assertions to validate the response data

def test_get_proposed_change(client):
    # Create a test proposed change first and get its ID
    created_response = client.post('/proposed/changes', data = {
        'data': json.dumps({
            'official_name': 'New Satellite',
            'reg_country': 'USA',
            'own_country': 'USA',
            'owner_name': 'Owner Name',
            'user_type': 'User Type',
            'purposes': 'Purposes',
            'detailed_purpose': 'Detailed Purpose',
            'orbit_class': 'Orbit Class',
            'orbit_type': 'Orbit Type',
            'geo_longitude': 0,
            'perigee': 497,
            'apogee': 517,
            'eccentricity': 0.00145,
            'inclination': 97.45,
            'period_min': 94.7,
            'mass_launch': 5,
            'mass_dry': 50,
            'power_watts': 4.5,
            'launch_date': '2023-10-29',
            'exp_lifetime': 2,
            'contractor': 'Contractor',
            'contractor_country': 'Contractor Country',
            'launch_site': 'Launch Site',
            'launch_vehicle': 'Launch Vehicle',
            'cospar': "2017-036L",
            'norad': 42775,
            'comment_note': 'Comment Note',
            'source_orbit': 'Source Orbit',
            'source_satellite': ['Source Satellite']
        }),
        'proposed_user': 'Test User',
        'created_at': '2023-10-29',
        'proposed_notes': 'Test Notes',
    })
    created_data = created_response.get_json()
    print(created_data)
    created_id = created_data['id']  # Use get_json() to access the JSON response

    response = client.get(f'/proposed/changes/{created_id}')
    assert response.status_code == 200  # Check for a successful retrieval
    response_data = json.loads(response.data)
    # Add more assertions to validate the response data

def test_get_proposed_change_not_found(client):
    random_id = 123456789
    response = client.get(f'/proposed/changes/{random_id}')
    assert response.status_code == 404  # Check for a failed retrieval

def test_update_proposed_change(client):
    # Create a test proposed change first and get its ID
    created_response = client.post('/proposed/changes', data = {
        'data': json.dumps({
            'official_name': 'New Satellite',
            'reg_country': 'USA',
            'own_country': 'USA',
            'owner_name': 'Owner Name',
            'user_type': 'User Type',
            'purposes': 'Purposes',
            'detailed_purpose': 'Detailed Purpose',
            'orbit_class': 'Orbit Class',
            'orbit_type': 'Orbit Type',
            'geo_longitude': 0,
            'perigee': 497,
            'apogee': 517,
            'eccentricity': 0.00145,
            'inclination': 97.45,
            'period_min': 94.7,
            'mass_launch': 5,
            'mass_dry': 50,
            'power_watts': 4.5,
            'launch_date': '2023-10-29',
            'exp_lifetime': 2,
            'contractor': 'Contractor',
            'contractor_country': 'Contractor Country',
            'launch_site': 'Launch Site',
            'launch_vehicle': 'Launch Vehicle',
            'cospar': "2017-036L",
            'norad': 42775,
            'comment_note': 'Comment Note',
            'source_orbit': 'Source Orbit',
            'source_satellite': ['Source Satellite']
        }),
        'proposed_user': 'Test User',
        'created_at': '2023-10-29',
        'proposed_notes': 'Test Notes',
    })
    created_data = created_response.get_json()
    print(created_data)
    created_id = created_data['id']  # Use get_json() to access the JSON response


    # Update the created proposed change
    updated_data = {
        'data': json.dumps({
            'official_name': 'Updated Satellite',
            'reg_country': 'Canada',
            'own_country': 'Canada',
            'owner_name': 'Owner Name',
            'user_type': 'User Type',
            'purposes': 'Purposes',
            'detailed_purpose': 'Detailed Purpose',
            'orbit_class': 'Orbit Class',
            'orbit_type': 'Orbit Type',
            'geo_longitude': 0,
            'perigee': 497,
            'apogee': 517,
            'eccentricity': 0.00145,
            'inclination': 97.45,
            'period_min': 94.7,
            'mass_launch': 5,
            'mass_dry': 50,
            'power_watts': 4.5,
            'launch_date': '2023-10-29',
            'exp_lifetime': 2,
            'contractor': 'Contractor',
            'contractor_country': 'Contractor Country',
            'launch_site': 'Launch Site',
            'launch_vehicle': 'Launch Vehicle',
            'cospar': "2017-036L",
            'norad': 42775,
            'comment_note': 'Comment Note',
            'source_orbit': 'Source Orbit',
            'source_satellite': ['Source Satellite']
        }),
        'proposed_user': 'Updated User',
        'created_at': '2023-10-30',
        'proposed_notes': 'Updated Notes',
    }

    response = client.put(f'/proposed/changes/{created_id}', data=updated_data)
    assert response.status_code == 200  # Check for a successful update
    response_data = json.loads(response.data)
    assert 'id' in response_data  # Check if the response contains the ID of the updated proposed change


def test_approve_proposed_change(client):
    # Create a test proposed change first and get its ID
    created_response = client.post('/proposed/changes', data = {
        'data': json.dumps({
            'official_name': 'New Satellite',
            'reg_country': 'USA',
            'own_country': 'USA',
            'owner_name': 'Owner Name',
            'user_type': 'User Type',
            'purposes': 'Purposes',
            'detailed_purpose': 'Detailed Purpose',
            'orbit_class': 'Orbit Class',
            'orbit_type': 'Orbit Type',
            'geo_longitude': 0,
            'perigee': 497,
            'apogee': 517,
            'eccentricity': 0.00145,
            'inclination': 97.45,
            'period_min': 94.7,
            'mass_launch': 5,
            'mass_dry': 50,
            'power_watts': 4.5,
            'launch_date': '2023-10-29',
            'exp_lifetime': 2,
            'contractor': 'Contractor',
            'contractor_country': 'Contractor Country',
            'launch_site': 'Launch Site',
            'launch_vehicle': 'Launch Vehicle',
            'cospar': "2017-036L",
            'norad': 42775,
            'comment_note': 'Comment Note',
            'source_orbit': 'Source Orbit',
            'source_satellite': ['Source Satellite']
        }),
        'proposed_user': 'Test User',
        'created_at': '2023-10-29',
        'proposed_notes': 'Test Notes',
    })
    created_data = created_response.get_json()
    created_id = created_data['id']  # Use get_json() to access the JSON response

    # Approve the created proposed change
    response = client.put(f'/proposed/changes/approve/{created_id}')
    assert response.status_code == 200  # Check for a successful approval
    response_data = json.loads(response.data)
    assert 'id' in response_data  # Check if the response contains the ID of the approved proposed change


def test_deny_proposed_change(client):
    # Create a test proposed change first and get its ID
    created_response = client.post('/proposed/changes', data = {
        'data': json.dumps({
            'official_name': 'New Satellite',
            'reg_country': 'USA',
            'own_country': 'USA',
            'owner_name': 'Owner Name',
            'user_type': 'User Type',
            'purposes': 'Purposes',
            'detailed_purpose': 'Detailed Purpose',
            'orbit_class': 'Orbit Class',
            'orbit_type': 'Orbit Type',
            'geo_longitude': 0,
            'perigee': 497,
            'apogee': 517,
            'eccentricity': 0.00145,
            'inclination': 97.45,
            'period_min': 94.7,
            'mass_launch': 5,
            'mass_dry': 50,
            'power_watts': 4.5,
            'launch_date': '2023-10-29',
            'exp_lifetime': 2,
            'contractor': 'Contractor',
            'contractor_country': 'Contractor Country',
            'launch_site': 'Launch Site',
            'launch_vehicle': 'Launch Vehicle',
            'cospar': "2017-036L",
            'norad': 42775,
            'comment_note': 'Comment Note',
            'source_orbit': 'Source Orbit',
            'source_satellite': ['Source Satellite']
        }),
        'proposed_user': 'Test User',
        'created_at': '2023-10-29',
        'proposed_notes': 'Test Notes',
    })
    created_data = created_response.get_json()
    created_id = created_data['id']  # Use get_json() to access the JSON response

    # Deny the created proposed change
    response = client.put(f'/proposed/changes/deny/{created_id}')
    assert response.status_code == 200  # Check for a successful denial
    response_data = json.loads(response.data)
    assert 'id' in response_data  # Check if the response contains the ID of the denied proposed change



def test_save_all_approved_or_denied_changes(client):    
    # Create a test proposed change that is approved
    approved_data = {
        'data': json.dumps({
            'official_name': 'Approved Test Satellite1',
            'reg_country': 'USA',
            'own_country': 'USA',
            'owner_name': 'Approved Owner',
            'user_type': 'Approved User Type',
            'purposes': 'Approved Purposes',
            'detailed_purpose': 'Approved Detailed Purpose',
            'orbit_class': 'Approved Orbit Class',
            'orbit_type': 'Approved Orbit Type',
            'geo_longitude': 45.6789,
            'perigee': 400,
            'apogee': 800,
            'eccentricity': 0.00123,
            'inclination': 98.76,
            'period_min': 120.5,
            'mass_launch': 10,
            'mass_dry': 100,
            'power_watts': 7.5,
            'launch_date': '2023-10-29',
            'exp_lifetime': 5,
            'contractor': 'Approved Contractor',
            'contractor_country': 'Approved Contractor Country',
            'launch_site': 'Approved Launch Site',
            'launch_vehicle': 'Approved Launch Vehicle',
            'cospar': "2023-045A",
            'norad': 98765,
            'comment_note': 'Approved Comment Note',
            'source_orbit': 'Approved Source Orbit',
            'source_satellite': ['Approved Source Satellite'],
        }),
        'proposed_user': 'Test User',
        'created_at': '2023-10-29',
        'proposed_notes': 'Test Notes',
    }

    approved_response = client.post('/proposed/changes', data=approved_data)
    approved_res = approved_response.get_json()
    approved_id = approved_res['id']

    # approve the approved change
    client.put(f'/proposed/changes/approve/{approved_id}')

    # Create a test proposed change that is denied
    denied_data = {
        'data': json.dumps({
            'official_name': 'Denied Test Satellite',
            'reg_country': 'USA',
            'own_country': 'USA',
            'owner_name': 'Denied Owner',
            'user_type': 'Denied User Type',
            'purposes': 'Denied Purposes',
            'detailed_purpose': 'Denied Detailed Purpose',
            'orbit_class': 'Denied Orbit Class',
            'orbit_type': 'Denied Orbit Type',
            'geo_longitude': 33.1234,
            'perigee': 300,
            'apogee': 700,
            'eccentricity': 0.001,
            'inclination': 96.54,
            'period_min': 110.2,
            'mass_launch': 9,
            'mass_dry': 90,
            'power_watts': 6.5,
            'launch_date': '2023-10-29',
            'exp_lifetime': 4,
            'contractor': 'Denied Contractor',
            'contractor_country': 'Denied Contractor Country',
            'launch_site': 'Denied Launch Site',
            'launch_vehicle': 'Denied Launch Vehicle',
            'cospar': "2023-046B",
            'norad': 87654,
            'comment_note': 'Denied Comment Note',
            'source_orbit': 'Denied Source Orbit',
            'source_satellite': ['Denied Source Satellite'],
        }),
        'proposed_user': 'Test User',
        'created_at': '2023-10-29',
        'proposed_notes': 'Test Notes',
    }

    denied_response = client.post('/proposed/changes', data=denied_data)
    denied_res = denied_response.get_json()
    denied_id = denied_res['id']

    # deny the denied change
    client.put(f'/proposed/changes/deny/{denied_id}')

    # Create a test proposed change that is neither approved nor denied
    pending_data = {
        'data': json.dumps({
            'official_name': 'Pending Satellite',
            'reg_country': 'USA',
            'own_country': 'USA',
            'owner_name': 'Pending Owner',
            'user_type': 'Pending User Type',
            'purposes': 'Pending Purposes',
            'detailed_purpose': 'Pending Detailed Purpose',
            'orbit_class': 'Pending Orbit Class',
            'orbit_type': 'Pending Orbit Type',
            'geo_longitude': 12.3456,
            'perigee': 200,
            'apogee': 600,
            'eccentricity': 0.0005,
            'inclination': 99.32,
            'period_min': 85.3,
            'mass_launch': 8,
            'mass_dry': 80,
            'power_watts': 8.0,
            'launch_date': '2023-10-29',
            'exp_lifetime': 3,
            'contractor': 'Pending Contractor',
            'contractor_country': 'Pending Contractor Country',
            'launch_site': 'Pending Launch Site',
            'launch_vehicle': 'Pending Launch Vehicle',
            'cospar': "2023-047C",
            'norad': 76543,
            'comment_note': 'Pending Comment Note',
            'source_orbit': 'Pending Source Orbit',
            'source_satellite': ['Pending Source Satellite'],
        }),
        'proposed_user': 'Test User',
        'created_at': '2023-10-29',
        'proposed_notes': 'Test Notes',
    }

    pending_response = client.post('/proposed/changes', data=pending_data)
    pending_data = pending_response.get_json()
    pending_id = pending_data['id']

    # Call the API to persist approved and denied changes
    response = client.post('/proposed/changes/persist', data={'approved_user': 'Test User'})
    print(response.data)

    # Check that the API returns a 200 status code
    assert response.status_code == 200

    # Check that the message in the response confirms the persisted changes
    response_data = response.get_json()
    assert 'persisted' in response_data['message'].lower()

    # verify approved data is persisted properly
    approved_response = client.get(f'/proposed/changes/{approved_id}')
    assert approved_response.status_code == 200
    # check that the approved_data in proposed_table is marked as "persisted"
    approved_satellite_dict = approved_response.get_json()
    assert approved_satellite_dict['is_approved'] == 'persisted'

    # Check that the pending change still exists in the proposed_changes table
    pending_response = client.get(f'/proposed/changes/{pending_id}')
    assert pending_response.status_code == 200

    official_name = json.loads(approved_data["data"])["official_name"]
    # Check that the official_satellites table has been updated with approved changes
    # You can use the get API for the official_satellite to validate the update
    official_satellite_response = client.get(f'/confirmed/satellites/{official_name}')
    assert official_satellite_response.status_code == 200

    # check that the official_satellites_changelog has been updated with approved changes
    official_satellite_changelog_response = client.get('/edit/history')
    assert official_satellite_changelog_response.status_code == 200
    # check that the approved satellite name is in the response
    assert official_name in official_satellite_changelog_response.get_data(as_text=True)
