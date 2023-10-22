from flask import Blueprint, jsonify, request
from utils.helpers import get_db_connection

# Create a Blueprint for this subpath
confirmed_subpath = Blueprint('confirmed', __name__)

@confirmed_subpath.route('/satellites', methods=["GET"])
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
    
    # Calculate offset based on limit and page
    offset = (page - 1) * limit if limit else 0

    conn = get_db_connection()
    cursor = conn.cursor()

    # Modify the SQL query to use LIMIT, OFFSET, and ORDER BY for pagination and sorting
    query = "SELECT * FROM official_satellites"
    if sort_by:
        order = 'ASC' if asc else 'DESC'
        query += f" ORDER BY {sort_by} {order}"
    if limit:
        query += " LIMIT %s OFFSET %s"
        cursor.execute(query, (limit, offset))
    else:
        cursor.execute(query)
    
    satellites = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    # Convert the results to a list of dictionaries for JSON serialization
    columns = [desc[0] for desc in cursor.description]
    satellites_as_dict = [dict(zip(columns, row)) for row in satellites]

    return jsonify({'satellites': satellites_as_dict})