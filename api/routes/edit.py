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
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request

# Create a Blueprint for this subpath
edit_subpath = Blueprint('edit', __name__)

@edit_subpath.route('/<official_name>', methods=['PUT'])
@jwt_required()
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

    if not all(key in req_json for key in ['data', 'update_notes']):
        return jsonify({'error': 'Invalid request'}), 400

    data_dict = req_json['data']
    update_time = datetime.datetime.now()
    update_notes = req_json['update_notes']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Lets get the user's name from the JWT token
    verify_jwt_in_request()

    update_user_username = get_jwt_identity()
    # get full name from db
    cursor.execute("SELECT name FROM users WHERE username = %s", (update_user_username,))
    update_user_fullnames = cursor.fetchone()
    if update_user_fullnames:
        update_user = update_user_fullnames[0] + " (" + update_user_username + ")"
    else:
        update_user = f"Unknown ({update_user_username})" # mostly for testing, as this should never happen 
   
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
@jwt_required()
def get_all():
    """
    Retrieve all records from the official_satellites_changelog table with optional pagination and filtering.

    URL Parameters:
        - limit (optional): An integer specifying the number of records to return.
            If not provided, all records are returned.
        - page (optional): An integer specifying the page number when using pagination.
            Defaults to 1 if not provided. Used in conjunction with the 'limit' parameter 
            to determine the records offset.
        - sort_by (optional): A string specifying the column name to sort by.
            Defaults to a specific column if not provided.
        - asc (optional): A boolean value specifying the sort order.
            Defaults to False if not provided.
        - search (optional): A string specifying the search term to filter by.
        - search_column (optional): A string specifying the column to search in. Default is a specific column

    Example Usage:
        GET /edit/history?limit=10&page=2
        GET /edit/history?search=term&search_column=column_name
    """

    # Get the optional limit, page, sort_by, and asc parameters from the request URL
    limit = request.args.get('limit', default=None, type=int)
    page = request.args.get('page', default=1, type=int)
    sort_by = request.args.get('sort_by', default='update_time', type=str)
    asc = request.args.get('asc', default=False, type=lambda v: v.lower() == 'true')
    search = request.args.get('search', default=None, type=str)
    search_column = request.args.get('search_column', default='official_name', type=str)  # Replace 'default_search_column'
    
    # Calculate offset based on limit and page
    offset = (page - 1) * limit if limit else 0

    conn = get_db_connection()
    cursor = conn.cursor()

    # Modify the SQL query to use LIMIT, OFFSET, and ORDER BY for pagination and sorting
    query = "SELECT * FROM official_satellites_changelog"
    params = []

    if search:
        search_term = f"%{search}%"
        query += f" WHERE CAST({search_column} AS TEXT) ILIKE %s"
        params.append(search_term)

    if sort_by:
        order = 'ASC' if asc else 'DESC'
        query += f" ORDER BY {sort_by} {order}, official_name DESC"
    else:
        query += " ORDER BY official_name DESC"

    if limit is not None:
        query += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])

    cursor.execute(query, tuple(params))
    records = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    # Convert the results to a list of dictionaries for JSON serialization
    columns = [desc[0] for desc in cursor.description]
    records_as_dict = [dict(zip(columns, row)) for row in records]

    return jsonify({'satellites': records_as_dict}), 200

#TODO: choose an approriate one from export to csv/excel
@edit_subpath.route('/history/export/csv', methods=['GET'])
@jwt_required()
def export_history_to_csv():
    """
    Export all records from the official_satellites_changelog table to a CSV file.

    Parameters:
        - None

    Returns:
        A CSV file containing the changelog data.

    Example Usage:
        GET /edit/history/csv
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

@edit_subpath.route('/history/export/xlsx', methods=['GET'])
@jwt_required()
def export_history_to_excel():
    """
    Export all records from the official_satellites_changelog table to an Excel file.

    Parameters:
        - None

    Returns:
        An Excel file containing the changelog data.
    
    Example Usage:
        GET /edit/history/xlsx
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # The SQL query to retrieve all satellites
    cursor.execute("SELECT * FROM official_satellites_changelog")
    records = cursor.fetchall()

    # A new Excel workbook and the active worksheet
    wb = Workbook()
    ws = wb.active

   # Using cursor.description to get column headers
    if cursor.description:
        column_headers = [desc[0] for desc in cursor.description]
       # print("Column Headers:", column_headers)  
        ws.append(column_headers)  # Append the column headers to the worksheet

    # Append each record as a new row in the worksheet
    for record in records:
        #print("Raw Record:", record) 
        processed_record = []
        for item in record:
            if isinstance(item, list):
                # Convert lists to JSON strings
                processed_record.append(json.dumps(item))
            else:
                processed_record.append(str(item) if item is not None else '')
        # print("Processed Record:", processed_record)
        ws.append(processed_record)

    # Save the workbook 
    excel_file = BytesIO()
    wb.save(excel_file)
    excel_file.seek(0)

    cursor.close()
    conn.close()

    return send_file(
                excel_file, 
                as_attachment=True, 
                download_name='changelog.xlsx', 
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
