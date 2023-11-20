import pytest
from app import app
from utils.helpers import get_db_connection
from datetime import datetime
import csv
from io import StringIO
from sqlalchemy import text
from utils.helpers import SessionLocal
import openpyxl
import io
import json


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


def test_export_history_to_csv(client):
    # Test exporting changelog to CSV
    response = client.get('/edit/history/export/csv')
    assert response.status_code == 200
    assert response.content_type == 'text/csv'

    csv_data = response.data.decode('utf-8').splitlines()
    reader = csv.reader(StringIO('\n'.join(csv_data)))
    rows = [row for row in reader]
    header, *rows = rows

    # Fetch data
    session = SessionLocal()
    try:
        result = session.execute(text("SELECT * FROM official_satellites_changelog"))
        db_rows = result.fetchall()
        db_header = result.keys()

        # Compare the headers and rows
        assert header == db_header
        for csv_row, db_row in zip(rows, db_rows):
            db_row_str = [str(item) if item is not None else '' for item in db_row]
            assert csv_row == db_row_str

    finally:
        session.close()


def test_export_history_to_excel(client):
    # Test exporting changelog to Excel (xlsx)
    response = client.get('/edit/history/export/xlsx')
    assert response.status_code == 200
    assert response.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    
    # Helper functions to deal with float comparision
    def is_float(value):
        if value is None: # deal with none
            return False
        try:
            float(value)
            return True
        except ValueError:
            return False
    # Helper functions to deal with float comparision
    def almost_equal(a, b, tol=1e-5):
        if a is None or b is None:
            return a == b
        try:
            return abs(float(a) - float(b)) < tol
        except ValueError:
            return False

    excel_data = io.BytesIO(response.data)
    workbook = openpyxl.load_workbook(excel_data)
    worksheet = workbook.active
    excel_rows = list(worksheet.rows)

    headers = [cell.value for cell in excel_rows[0]]
    excel_data_rows = [[cell.value for cell in row] for row in excel_rows[1:]]

    session = SessionLocal()
    try:
        result = session.execute(text("SELECT * FROM official_satellites_changelog"))
        db_rows = result.fetchall()
        db_header = result.keys()

        # Compare the headers with the database
        assert headers == db_header

        # Compare the rows with the database
        for excel_row, db_row in zip(excel_data_rows, db_rows):
            for i, (excel_item, db_item) in enumerate(zip(excel_row, db_row)):
                # Deserialization and numeric conversion
                # print(f"Excel Row {i}, Excel item: {excel_item}")
                # print(f"DB Row {i}, Excel item: {db_item}")
                if excel_item is not None:
                    try:
                        excel_item = json.loads(excel_item.replace("'", '"'))
                        if is_float(excel_item): 
                            excel_item = float(excel_item)
                    except (TypeError, json.JSONDecodeError):
                        if isinstance(excel_item, str) and excel_item.replace('.', '', 1).isdigit():
                            excel_item = float(excel_item)
                        else:
                            excel_item = str(excel_item)
                
                # Nnumeric conversion)
                if db_item is not None and isinstance(db_item, str) and db_item.replace('.', '', 1).isdigit():
                    db_item = float(db_item)
                else:
                    db_item = str(db_item) if db_item is not None else None

                # Compare the processed items
                if is_float(excel_item) or is_float(db_item):
                    assert almost_equal(excel_item, db_item), f"Mismatch at row {i}: Excel '{excel_item}' != DB '{db_item}'"
                else:
                    assert excel_item == db_item, f"Mismatch at row {i}: Excel '{excel_item}' != DB '{db_item}'"
                   
    finally:
        session.close()