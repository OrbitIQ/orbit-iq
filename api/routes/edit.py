from flask import Blueprint, jsonify, request
from utils.helpers import get_db_connection

# Create a Blueprint for this subpath
edit_subpath = Blueprint('edit', __name__)

@edit_subpath.route('/int:satellite_id', methods=['PUT'])
def update(satellite_id):
    """
     Update a record in the official_satellites table.

    Parameters:
        - satellite_id (int): The unique identifier of the satellite to update.

    Request Data:
        - data (str): The updated data for the satellite.
        - source (str): The updated source for the satellite.

    Returns:
        A JSON response indicating the success or failure of the update.

    Example Usage:
        PUT /edit/<valid_satellite_id>
        Body: data=new_data & source=new_source

    Returns:
        A JSON representation of the edited satellite records
    """
    data = request.form['data']
    source = request.form['source']

    conn = get_db_connection()
    cursor = conn.cursor()

    # The SQL query to update the official_satellites table
    update_query = "UPDATE official_satellites SET data = %s, source = %s WHERE id = %s"
    cursor.execute(update_query, (data, source, satellite_id))

    # The SQL query to retrieve data and source
    cursor.execute("SELECT data, source FROM official_satellites WHERE id = %s", (satellite_id))
    edited_data, edited_source = cursor.fetchone()

     # The SQL query to create log table if it doesn't exist.
    create_log_table_query = """
        CREATE TABLE IF NOT EXISTS official_satellite_changelog (
            official_name VARCHAR(255) PRIMARY KEY,
            action VARCHAR(10),
            log_data VARCHAR(255),
            source text
        )
    """
    cursor.execute(create_log_table_query)

    # The SQL query to insert a log into the official_satellite_changelog table
    log_query = "INSERT INTO official_satellite_changelog (satellite_id, action, data, source) VALUES (%s, 'edit', %s, %s)"
    cursor.execute(log_query, (satellite_id, data, source))

    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()

    return jsonify({'message': 'Edit successful', 'data': edited_data, 'source': edited_source})

