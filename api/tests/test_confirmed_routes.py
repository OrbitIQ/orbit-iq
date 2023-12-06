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
def mock_jwt_required():
    with patch('flask_jwt_extended.jwt_required', lambda fn: fn):
        yield

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

def test_export_to_excel(client):
    """Test the export functionality."""
    # Increase the field size limit for csv.reader
    csv.field_size_limit(sys.maxsize)

    # Request the export functionality
    response = client.get('/confirmed/satellites/export')
    
    # Validate the response and the exported file
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "text/csv"
    assert response.headers["Content-Disposition"] == "attachment; filename=confirmed_official_satellites.csv"
    
    def process_row(row):
        processed_row = []
        list_items = []
        in_list = False

        for item in row:
            if isinstance(item, str):
                if item.startswith('['):  # Start of a list or sublist
                    in_list = True
                    list_items.append(item.lstrip("["))
                elif in_list:
                    list_items.append(item.rstrip("]").rstrip(","))
                    if item.endswith(']') or item.endswith(']]'):  # End of a simple list
                        in_list = False
                        processed_list_items = [f"{i.strip()}" if i.strip() != 'None' else 'None' for i in list_items]
                        processed_list_str = ', '.join(processed_list_items)
                        processed_row.append(f"[{processed_list_str}]")
                        list_items = []
                else:
                    processed_row.append(item)
            else:  # If the item is not a string (e.g., a list), simply append it
                processed_row.append(item)

        if processed_row and isinstance(processed_row[-1], str) and processed_row[-1].startswith('"[') and processed_row[-1].endswith(']"'):
            processed_row[-1] = processed_row[-1][1:-1]
        return processed_row

    # Parse the CSV response data without using Pandas
    csv_data = response.data.decode('utf-8').splitlines()
    reader = csv.reader(csv_data)
    rows = [process_row(row) for row in reader]
    header, *rows = rows
    
    # Fetch data from the database using SQLAlchemy
    session = SessionLocal()
    try:
        result = session.execute(text("SELECT * FROM official_satellites"))
        db_rows = result.fetchall()
        db_header = result.keys()
        
        # Compare the headers
        assert header == db_header
        
        # Compare the rows
        for csv_row, db_row in zip(rows, db_rows):
            if csv_row != list(map(str, db_row)):
                print("Mismatch found!")
                print("CSV Row:", csv_row)
                print("DB Row: ", list(map(str, db_row)))
                assert csv_row == list(map(str, db_row))
    finally:
        session.close()
    


