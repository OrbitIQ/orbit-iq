from flask import Blueprint, jsonify, request
from utils.helpers import get_db_connection
from flask import Response
from utils.helpers import SessionLocal
from sqlalchemy import text
import csv
from io import StringIO
from flask_jwt_extended import jwt_required

# Create a Blueprint for this subpath
confirmed_subpath = Blueprint('confirmed', __name__)


@confirmed_subpath.route('/satellites', methods=["GET"])
@jwt_required()
def get_satellites():
    """
    Retrieve satellites from the official_satellites table with optional pagination.
    
    URL Parameters:
        - limit (optional): An integer specifying the number of records to return.
            If not provided, all records are returned.
        - page (optional): An integer specifying the page number when using pagination.
            Defaults to 1 if not provided. Used in conjunction with the 'limit' parameter 
            to determine the records offset.
        - sort_by (optional): A string specifying the column name to sort by.
            Defaults to 'launch_date' if not provided.
        - asc (optional): A boolean value specifying the sort order.
            Defaults to False if not provided.
        - search (optional): A string specifying the search term to filter by.
        - search_column (optional): A string specifying the column to search in. Default is 'official_name'

    Example Usage:
        - /confirmed/satellites?limit=10&page=2: Returns records 11-20
        - /confirmed/satellites?limit=5: Returns the first 5 records
        - /confirmed/satellites: Returns all records
        - /confirmed/satellites?sort_by=launch_date&asc=True: Returns all records sorted by launch_date in ascending order

    Returns:
        A JSON representation of the selected satellite records.
    """
    
    # Get the optional limit, page, sort_by, and asc parameters from the request URL
    limit = request.args.get('limit', default=None, type=int)
    page = request.args.get('page', default=1, type=int)
    sort_by = request.args.get('sort_by', default='launch_date', type=str)
    asc = request.args.get('asc', default=False, type=lambda v: v.lower() == 'true')
    search = request.args.get('search', default=None, type=str)
    search_column = request.args.get('search_column', default='official_name', type=str)
    
    # Calculate offset based on limit and page
    offset = (page - 1) * limit if limit else 0

    conn = get_db_connection()
    cursor = conn.cursor()

    # Modify the SQL query to use LIMIT, OFFSET, and ORDER BY for pagination and sorting
    query = "SELECT * FROM official_satellites"

    params = []
    if search:
        # use where & ilike to search for the term search
        search_term = f"%{search}%"
        query += f" WHERE CAST({search_column} AS TEXT) ILIKE %s"
        params.append(search_term)

    if sort_by:
        order = 'ASC' if asc else 'DESC'
        query += f" ORDER BY {sort_by} {order}, official_name DESC"
    else:
        query += " ORDER BY launch_date DESC, official_name DESC"

    if limit is not None:
        query += " LIMIT %s OFFSET %s"
        params.extend([limit, offset])
  
    cursor.execute(query, tuple(params))
    satellites = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    # Convert the results to a list of dictionaries for JSON serialization
    columns = [desc[0] for desc in cursor.description]
    satellites_as_dict = [dict(zip(columns, row)) for row in satellites]

    return jsonify({'satellites': satellites_as_dict})

# Add a route to retrieve a satellite by name
@confirmed_subpath.route('/satellites/<official_name>', methods=["GET"])
@jwt_required()
def get_satellite_by_name(official_name):
    """
    Retrieve a satellite from the official_satellites table by name.

    Parameters:
        - official_name (str): The name of the satellite to retrieve.

    Example Usage:
        - /confirmed/satellites/Starlink: Returns the Starlink satellite record

    Returns:
        A JSON representation of the selected satellite record.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # The SQL query to retrieve a satellite by name
    cursor.execute("SELECT * FROM official_satellites WHERE official_name = %s", (official_name,))
    satellite = cursor.fetchone()
    # If the satellite is not found, return a 404 error
    if not satellite:
        return jsonify({'error': 'Satellite not found'}), 404

    # Close the connection
    cursor.close()
    conn.close()

    # Convert the results to a dictionary for JSON serialization
    columns = [desc[0] for desc in cursor.description]
    satellite_as_dict = dict(zip(columns, satellite))

    return jsonify({'satellite': satellite_as_dict}), 200

@confirmed_subpath.route('/satellites/export', methods=["GET"])
@jwt_required()
def export_to_excel():
    """
    Export the official_satellites data to an Excel file and return it as a downloadable response.

    Returns:
        A CSV file of the confirmed satellite record.
    """
    # Connect to the database and fetch all records from the official_satellites table
       # Connect to the database
       # Connect to the database and fetch all records from the official_satellites table
    # Connect to the database
    session = SessionLocal()

    try:
        # Fetch all records from the official_satellites table using SQLAlchemy
        result = session.execute(text("SELECT * FROM official_satellites"))
        
        # Get column names and rows
        columns = result.keys()
        rows = result.fetchall()

        processed_rows = []
        for row in rows:
            # Convert the 2D array (last item) into a proper string representation
            if isinstance(row[-1], list):  # Check for 2D array
                array_str_items = []
                for item in row[-1]:
                    if item is not None:
                        array_str_items.append(f"'{item}'")  # Wrap non-None items with single quotes
                    else:
                        array_str_items.append("None")
                array_str = '"'+'[' + ', '.join(array_str_items) + ']'+ '"'
                row = list(row[:-1]) + [array_str]
            
            # Process the rest of the row
            processed_row = [value if value is not None else "None" for value in row]
            processed_rows.append(processed_row)
             
        # Convert the results to CSV format
        csv_data = ",".join(columns) + "\n"  # Column headers
        for row in processed_rows[0:5]:
            csv_data += ",".join([str(element) for element in row]) + "\n"

        output = StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
        writer.writerows(processed_rows)

        csv_data += output.getvalue()
        
        # Create a response with the CSV data
        response = Response(csv_data, content_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=confirmed_official_satellites.csv"
        
        return response
    
    finally:
        session.close() 
        
# TODO: test only. Remove before production
# Delete a satellite by name
# Note: This route is for Testing purpose only, deleting test data from the official table is not allowed. 
# It is not meant to be part of the API. DO NOT USE THIS IN PRODUCTION
@confirmed_subpath.route('/satellites/<official_name>', methods=["DELETE"])
@jwt_required()
def delete_satellite_by_name(official_name):
    # DO NOT USE THIS IN PRODUCTION
    conn = get_db_connection()
    cursor = conn.cursor()

    # The SQL query to delete a satellite by name
    cursor.execute("DELETE FROM official_satellites WHERE official_name = %s", (official_name,))
    
    # Commit the transaction to persist the deletion
    conn.commit()

    # If the satellite is not found, return a 404 error
    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return jsonify({'error': 'Satellite not found'}), 404

    # Close the connection
    cursor.close()
    conn.close()

    return jsonify({'message': 'Satellite deleted successfully'}), 200