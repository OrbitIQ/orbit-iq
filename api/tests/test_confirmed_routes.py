import pytest
from app import app
from utils.helpers import get_db_connection
from datetime import datetime
from utils.helpers import SessionLocal
from sqlalchemy import text
import csv
import sys
from unittest.mock import patch

# This fixture will be used by the tests to send requests to the application
@pytest.fixture(autouse=True)
def neuter_jwt(monkeypatch):
    def no_verify(*args, **kwargs):
        pass

    from flask_jwt_extended import view_decorators, verify_jwt_in_request
    from flask_jwt_extended import utils 

    monkeypatch.setattr(view_decorators, 'verify_jwt_in_request', no_verify)
    monkeypatch.setattr(view_decorators, 'jwt_required', no_verify)
    monkeypatch.setattr(utils, 'get_jwt_identity', lambda: 'test_user')
    
    from flask_jwt_extended import verify_jwt_in_request, jwt_required, get_jwt_identity
    monkeypatch.setattr('flask_jwt_extended.verify_jwt_in_request', no_verify)
    monkeypatch.setattr('flask_jwt_extended.jwt_required', no_verify)
    monkeypatch.setattr('flask_jwt_extended.get_jwt_identity', lambda: 'test_user')


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_all_satellites(client):
    """Test getting all satellites without pagination."""
    response = client.get('/confirmed/satellites')
    print(response)
    assert response.status_code == 200
    data = response.get_json()
    assert 'satellites' in data

def test_get_satellites_with_name(client):
    """Test getting satellites with name."""
    response = client.get('/confirmed/satellites/Aalto-1')
    assert response.status_code == 200
    data = response.get_json()
    assert 'satellite' in data
    satellite = data['satellite']
    assert 'Aalto-1' in satellite['official_name']

def test_get_satellites_with_name_not_found(client):
    """Test getting satellites with name not found."""
    response = client.get('/confirmed/satellites/Not-Found')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
    assert 'Satellite not found' in data['error']

def test_get_satellites_with_pagination(client):
    """Test getting satellites with pagination."""
    response = client.get('/confirmed/satellites?limit=5&page=2')
    assert response.status_code == 200
    data = response.get_json()
    assert 'satellites' in data
    assert len(data['satellites']) == 5

def test_database_connection():
    """Test database connection."""
    conn = get_db_connection()
    assert conn is not None
    conn.close()

def test_sort_by_and_asc_parameters(client):
    """Test sorting satellites with sort_by and asc parameters."""
    # Sort by launch_date in ascending order
    response = client.get('/confirmed/satellites?sort_by=launch_date&asc=True')
    assert response.status_code == 200
    data = response.get_json()
    assert 'satellites' in data
    satellites = data['satellites']
    sorted_satellites = sorted(
        satellites,
        key=lambda x: datetime.strptime(x['launch_date'], '%a, %d %b %Y %H:%M:%S GMT') if x['launch_date'] is not None else datetime.min
    )
    assert satellites == sorted_satellites

    # Sort by launch_date in descending order
    response = client.get('/confirmed/satellites?sort_by=launch_date&asc=False')
    assert response.status_code == 200
    data = response.get_json()
    assert 'satellites' in data
    satellites = data['satellites']
    sorted_satellites = sorted(
        satellites,
        key=lambda x: datetime.strptime(x['launch_date'], '%a, %d %b %Y %H:%M:%S GMT') if x['launch_date'] is not None else datetime.min,
        reverse=True
    )
    assert satellites == sorted_satellites
