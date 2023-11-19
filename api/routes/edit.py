from flask import Blueprint, jsonify, request
from utils.helpers import get_db_connection
import datetime
import json
import logging
from flask import send_file
from openpyxl import Workbook
from io import BytesIO
from flask import Response
import csv
from io import StringIO

# Create a Blueprint for this subpath
edit_subpath = Blueprint('edit', __name__)

@edit_subpath.route('/<official_name>', methods=['PUT'])
def update(official_name):
    """
    Update a record in the official_satellites table.

    Parameters:
        - satellite_id (str): The unique identifier of the satellite to update.

    Request Data:
        - data (str): The updated data for the satellite.
            - "offical_name": 
            - "reg_country":
            - "own_country":
            ...
        - update_user (str): The user who is updating the satellite record.
        - update_notes (str): Notes about the update.

    Returns:
        A JSON response indicating the success or failure of the update.

    Example Usage:
        PUT /edit/<official_name>
        Body: data=new_data & source=new_source

    Returns:
        A JSON representation of the edited satellite records
    """

    if not request.is_json:
        return jsonify({'error': 'Request data is not in JSON format'}), 400

    req_json = request.get_json()

    if not all(key in req_json for key in ['data', 'update_user', 'update_notes']):
        return jsonify({'error': 'Invalid request'}), 400

    data_dict = req_json['data']
    update_user = req_json['update_user']
    update_time = datetime.datetime.now()
    update_notes = req_json['update_notes']

    conn = get_db_connection()
    cursor = conn.cursor()

    # retrieve old data to be logged
    print('hi')
   
    retrieve_old_data = "SELECT * FROM official_satellites WHERE official_name = %s"
    cursor.execute(retrieve_old_data, (official_name,))
    old_data = cursor.fetchone()
    # If the satellite is not found, return a 404 error
    if not old_data:
        return jsonify({'error': 'Satellite not found'}), 404

    # serialize old_data
    columns = [desc[0] for desc in cursor.description]
    old_data_as_dict = dict(zip(columns, old_data))

    # The SQL query to update the official_satellites table
    update_query = update_query = """
    UPDATE official_satellites SET reg_country = %s, own_country = %s, owner_name = %s, user_type = %s, purposes = %s, 
    detailed_purpose = %s, orbit_class = %s, orbit_type = %s, geo_longitude = %s, perigee = %s, apogee = %s, eccentricity = %s, inclination = %s, period_min = %s, mass_launch = %s, 
    mass_dry = %s, power_watts = %s, launch_date = %s, exp_lifetime = %s, contractor = %s, contractor_country = %s, launch_site = %s, launch_vehicle = %s, cospar = %s, 
    norad = %s, comment_note = %s, source_orbit = %s, source_satellite = %s WHERE official_name = %s
    """
    cursor.execute(update_query, 
    (data_dict['reg_country'], data_dict['own_country'], data_dict['owner_name'], data_dict['user_type'], 
    data_dict['purposes'], data_dict['detailed_purpose'], data_dict['orbit_class'], data_dict['orbit_type'], data_dict['geo_longitude'], 
    data_dict['perigee'], data_dict['apogee'], data_dict['eccentricity'], data_dict['inclination'], data_dict['period_min'], 
    data_dict['mass_launch'], data_dict['mass_dry'], data_dict['power_watts'], data_dict['launch_date'], data_dict['exp_lifetime'], 
    data_dict['contractor'], data_dict['contractor_country'], data_dict['launch_site'], data_dict['launch_vehicle'], data_dict['cospar'], 
    data_dict['norad'], data_dict['comment_note'], data_dict['source_orbit'], data_dict['source_satellite'], official_name))

    # The SQL query to retrieve data and source
    cursor.execute("SELECT * FROM official_satellites WHERE official_name = %s", (official_name,))
    updated_data = cursor.fetchone()
    if not updated_data:
        return jsonify({'error': 'unknown error from update'}), 500

    # The SQL query to insert a log into the official_satellite_changelog table
    log_query = """
    INSERT INTO official_satellites_changelog (update_user, update_action, update_time, update_notes, official_name, 
    reg_country, own_country, owner_name, user_type, purposes, detailed_purpose, orbit_class, orbit_type, geo_longitude, perigee, apogee, 
    eccentricity, inclination, period_min, mass_launch, mass_dry, power_watts, launch_date, exp_lifetime, contractor, contractor_country, 
    launch_site, launch_vehicle, cospar, norad, comment_note, source_orbit, source_satellite) 
    VALUES (%s, 'edit', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(log_query, (update_user, update_time, update_notes, 
    old_data_as_dict['official_name'], old_data_as_dict['reg_country'], old_data_as_dict['own_country'], old_data_as_dict['owner_name'], old_data_as_dict['user_type'], 
    old_data_as_dict['purposes'], old_data_as_dict['detailed_purpose'], old_data_as_dict['orbit_class'], old_data_as_dict['orbit_type'], old_data_as_dict['geo_longitude'], 
    old_data_as_dict['perigee'], old_data_as_dict['apogee'], old_data_as_dict['eccentricity'], old_data_as_dict['inclination'], old_data_as_dict['period_min'], 
    old_data_as_dict['mass_launch'], old_data_as_dict['mass_dry'], old_data_as_dict['power_watts'], old_data_as_dict['launch_date'], old_data_as_dict['exp_lifetime'], 
    old_data_as_dict['contractor'], old_data_as_dict['contractor_country'], old_data_as_dict['launch_site'], old_data_as_dict['launch_vehicle'], old_data_as_dict['cospar'], 
    old_data_as_dict['norad'], old_data_as_dict['comment_note'], old_data_as_dict['source_orbit'], old_data_as_dict['source_satellite']))

    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()

    return jsonify({'message': 'Update successful', 'data': updated_data, "user": update_user, "time": update_time, "notes": update_notes}), 200


@edit_subpath.route('/history', methods=['GET'])
def get_all():
    """
    Retrieve all records from the official_satellites_changelog table.

    Parameters:
        - None

    Returns:
        A JSON representation of the satellite records.

    Example Usage:
        GET /edit/history
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # The SQL query to retrieve all satellites
    cursor.execute("SELECT * FROM official_satellites_changelog")
    satellites = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    # Convert the results to a list of dictionaries for JSON serialization
    columns = [desc[0] for desc in cursor.description]
    satellites_as_dict = [dict(zip(columns, row)) for row in satellites]

    return jsonify({'satellites': satellites_as_dict}), 200

#TODO: choose an approriate one from export to csv/excel
@edit_subpath.route('/history/export/csv', methods=['GET'])
def export_history_to_csv():
    """
    Export all records from the official_satellites_changelog table to a CSV file.

    Returns:
        A CSV file containing the changelog data.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
  # The SQL query to retrieve all satellites
    cursor.execute("SELECT * FROM official_satellites_changelog")
    records = cursor.fetchall()

    # Generate CSV data
    def generate():
        data = StringIO()
        writer = csv.writer(data)

        # Writing column headers
        if records:
            writer.writerow([desc[0] for desc in cursor.description])  # Column headers
            data.seek(0)
            yield data.read()
            data.seek(0)
            data.truncate(0)

        # Writing each row of data
        for record in records:
            writer.writerow(record)
            data.seek(0)
            yield data.read()
            data.seek(0)
            data.truncate(0)

    cursor.close()
    conn.close()

    # Return the CSV file as a downloadable response
    headers = {
        'Content-Disposition': 'attachment; filename=changelog.csv',
        'Content-Type': 'text/csv'
    }
    return Response(generate(), headers=headers)

    
