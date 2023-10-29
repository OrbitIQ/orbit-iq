from flask import Blueprint, jsonify, request
from utils.helpers import get_db_connection

# Create a Blueprint for this subpath
proposed_subpath = Blueprint('proposed', __name__)

# select * from proposed changes
@proposed_subpath.route('/changes', methods=["GET"])
def get_proposed():
    """
    Retrieve proposed changes from the proposed_changes table with optional pagination.
    
    URL Parameters:
        - limit (optional): An integer specifying the number of records to return.
            If not provided, all records are returned.
        - page (optional): An integer specifying the page number when using pagination.
            Defaults to 1 if not provided. Used in conjunction with the 'limit' parameter 
            to determine the records offset.
        - sort_by (optional): A string specifying the column name to sort by.
            Defaults to 'created_at' if not provided.
        - asc (optional): A boolean value specifying the sort order.
            Defaults to False if not provided.

    Example Usage:
        - /proposed/changes?limit=10&page=2: Returns records 11-20
        - /proposed/changes?limit=5: Returns the first 5 records
        - /proposed/changes: Returns all records
        - /proposed/changes?sort_by=created_at&asc=True: Returns all records sorted by created_at in ascending order

    Returns:
        A JSON representation of the selected proposed change records.
    """
    
    # Get the optional limit, page, sort_by, and asc parameters from the request URL
    limit = request.args.get('limit', default=None, type=int)
    page = request.args.get('page', default=1, type=int)
    sort_by = request.args.get('sort_by', default='created_at', type=str)
    asc = request.args.get('asc', default=False, type=lambda v: v.lower() == 'true')
    
    # Calculate offset based on limit and page
    offset = (page - 1) * limit if limit else 0

    conn = get_db_connection()
    cursor = conn.cursor()

    # Modify the SQL query to use LIMIT, OFFSET, and ORDER BY for pagination and sorting
    query = "SELECT * FROM proposed_changes"
    if sort_by:
        order = 'ASC' if asc else 'DESC'
        query += f" ORDER BY {sort_by} {order}"
    if limit:
        query += " LIMIT %s OFFSET %s"
        cursor.execute(query, (limit, offset))
    else:
        cursor.execute(query)
    
    proposed_changes = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    # Convert the results to a dictionary for JSON serialization
    columns = [desc[0] for desc in cursor.description]
    proposed_changes_list = [dict(zip(columns, record)) for record in proposed_changes]

    return jsonify({'proposed_changes': proposed_changes_list}), 200