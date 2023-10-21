import pytest
from app import app
from utils.helpers import get_db_connection
from datetime import datetime

# This fixture will be used by the tests to send requests to the application

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_get_all_satellites(client):
    """Test getting all satellites without pagination."""
    response = client.get('/confirmed/satellites')
    assert response.status_code == 200
    data = response.get_json()
    assert 'satellites' in data

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
