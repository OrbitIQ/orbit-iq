import json
import uuid
from flask import Blueprint, jsonify, request
from utils.helpers import get_db_connection
from psycopg2 import sql
import psycopg2
import datetime

proposed_changes_subpath = Blueprint('proposed_changes', __name__)

# TODO: might be good for future workflow like hitting edit on the frontend's production table actually creates a proposed change
# Create a new proposed change
@proposed_changes_subpath.route('/changes', methods=['POST'])
def create_proposed_change():
    """
    Request Data:
        - data (dict): The updated data for the satellite.
            - "offical_name": 
            - "reg_country":
            - "own_country":
            ...
        - proposed_user (str),
        - created_at (date),
        - proposed_notes (str),

    Example Usage:
        POST /proposed/changes
        Body: data=new_data & proposed_user=new_user & created_at=new_time & proposed_notes=new_notes
    
    Returns:
        - id (str): The ID of the newly created proposed change.
    """

    # Get data from request body
    data = request.form['data']
    proposed_user = request.form['proposed_user']
    created_at = request.form['created_at']
    proposed_notes = request.form['proposed_notes']
    #serialize data
    data_dict = json.loads(data)

    # Connect to PostgreSQL database
    conn = get_db_connection()

    # Create a cursor object
    cur = conn.cursor()
    # Execute SQL query to insert new proposed change, 34 fields
    query = sql.SQL("""INSERT INTO proposed_changes 
                    (proposed_user, created_at, proposed_notes, is_approved, official_name, 
                    reg_country, own_country, owner_name, user_type, purposes, detailed_purpose, orbit_class,
                     orbit_type, geo_longitude, perigee, apogee, eccentricity, inclination, period_min, mass_launch,
                     mass_dry, power_watts, launch_date, exp_lifetime, contractor, contractor_country, launch_site,
                     launch_vehicle, cospar, norad, comment_note, source_orbit, source_satellite) 
                    VALUES ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {},
                     {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {} ) RETURNING id;""").format(
        sql.Literal(proposed_user),
        sql.Literal(created_at),
        sql.Literal(proposed_notes),
        sql.Literal("pending"),
        sql.Literal(data_dict['official_name']),
        sql.Literal(data_dict['reg_country']),
        sql.Literal(data_dict['own_country']),
        sql.Literal(data_dict['owner_name']),
        sql.Literal(data_dict['user_type']),
        sql.Literal(data_dict['purposes']),
        sql.Literal(data_dict['detailed_purpose']),
        sql.Literal(data_dict['orbit_class']),
        sql.Literal(data_dict['orbit_type']),
        sql.Literal(data_dict['geo_longitude']),
        sql.Literal(data_dict['perigee']),
        sql.Literal(data_dict['apogee']),
        sql.Literal(data_dict['eccentricity']),
        sql.Literal(data_dict['inclination']),
        sql.Literal(data_dict['period_min']),
        sql.Literal(data_dict['mass_launch']),
        sql.Literal(data_dict['mass_dry']),
        sql.Literal(data_dict['power_watts']),
        sql.Literal(data_dict['launch_date']),
        sql.Literal(data_dict['exp_lifetime']),
        sql.Literal(data_dict['contractor']),
        sql.Literal(data_dict['contractor_country']),
        sql.Literal(data_dict['launch_site']),
        sql.Literal(data_dict['launch_vehicle']),
        sql.Literal(data_dict['cospar']),
        sql.Literal(data_dict['norad']),
        sql.Literal(data_dict['comment_note']),
        sql.Literal(data_dict['source_orbit']),
        sql.Literal(data_dict['source_satellite'])        
    )
    cur.execute(query)
    # Commit changes to database
    conn.commit()
    # Get ID of newly created proposed change
    id = cur.fetchone()[0]
    # Close database connection
    cur.close()
    conn.close()
    if id is None:
        return jsonify({'error': 'Unknown database issue.'}), 500
    # Return id of newly created proposed change
    return jsonify({'id': id}), 201

# select * from proposed changes
@proposed_changes_subpath.route('/changes', methods=["GET"])
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

    # For each row map the column -> value to a dictionary
    columns = [desc[0] for desc in cursor.description]
    proposed_changes = [dict(zip(columns, row)) for row in proposed_changes]

    return jsonify({'proposed_changes': proposed_changes})

# Get a specific proposed change by id
@proposed_changes_subpath.route('/changes/<id>', methods=['GET'])
def get_proposed_change(id):
    """
    Request Data:
        - None
    Example Usage:
        GET /proposed/changes/<id>
    """
    # Connect to PostgreSQL database
    conn = get_db_connection()

    # Create a cursor object
    cur = conn.cursor()
    # Execute SQL query to get proposed change by ID
    query = sql.SQL("SELECT * FROM proposed_changes WHERE id = {};").format(
        sql.Literal(id)
    )
    cur.execute(query)
    # Fetch one row from query result
    row = cur.fetchone()
    # Close database connection
    cur.close()
    conn.close()
    # If row is None, return 404 Not Found
    if row is None:
        return jsonify({'error': 'Proposed change not found.'}), 404
    # Otherwise, return proposed change as dictionary
    else:
        columns = [desc[0] for desc in cur.description]
        proposed_change_as_dict = dict(zip(columns, row))
        return jsonify(proposed_change_as_dict)

# Update a specific proposed change by ID
@proposed_changes_subpath.route('/changes/<id>', methods=['PUT'])
def update_proposed_change(id):
    """
    Request Data:
        - data (dict): The updated data for the satellite.
            - "offical_name": 
            - "reg_country":
            - "own_country":
            ...
        - proposed_user (str),
        - created_at (date),
        - proposed_notes (str),

    Example Usage:
        PUT /proposed/changes/<id>
        Body: data=new_data & proposed_user=new_user & created_at=new_time & proposed_notes=new_notes

    Returns:
        - id (str): The ID of the updated proposed change.
    """
    # Get data from request body
    data = request.form['data']
    proposed_user = request.form['proposed_user']
    created_at = request.form['created_at']
    proposed_notes = request.form['proposed_notes']
    #serialize data
    data_dict = json.loads(data)

    # Connect to PostgreSQL database
    conn = get_db_connection()

    # Create a cursor object
    cur = conn.cursor()
    # Execute SQL query to update proposed change by ID
    query = sql.SQL("""UPDATE proposed_changes SET 
                        proposed_user = {}, created_at = {}, proposed_notes = {},  is_approved = {},
                        official_name = {}, reg_country = {}, own_country = {}, owner_name = {}, user_type = {},
                        purposes = {}, detailed_purpose = {}, orbit_class = {}, orbit_type = {}, geo_longitude = {},
                        perigee = {}, apogee = {}, eccentricity = {}, inclination = {}, period_min = {},
                        mass_launch = {}, mass_dry = {}, power_watts = {}, launch_date = {}, exp_lifetime = {},
                        contractor = {}, contractor_country = {}, launch_site = {}, launch_vehicle = {},
                        cospar = {}, norad = {}, comment_note = {}, source_orbit = {}, source_satellite = {}
                        WHERE id = {} RETURNING id; 
                    """).format(
        sql.Literal(proposed_user),
        sql.Literal(created_at),
        sql.Literal(proposed_notes),
        sql.Literal("pending"),
        sql.Literal(data_dict['official_name']),
        sql.Literal(data_dict['reg_country']),
        sql.Literal(data_dict['own_country']),
        sql.Literal(data_dict['owner_name']),
        sql.Literal(data_dict['user_type']),
        sql.Literal(data_dict['purposes']),
        sql.Literal(data_dict['detailed_purpose']),
        sql.Literal(data_dict['orbit_class']),
        sql.Literal(data_dict['orbit_type']),
        sql.Literal(data_dict['geo_longitude']),
        sql.Literal(data_dict['perigee']),
        sql.Literal(data_dict['apogee']),
        sql.Literal(data_dict['eccentricity']),
        sql.Literal(data_dict['inclination']),
        sql.Literal(data_dict['period_min']),
        sql.Literal(data_dict['mass_launch']),
        sql.Literal(data_dict['mass_dry']),
        sql.Literal(data_dict['power_watts']),
        sql.Literal(data_dict['launch_date']),
        sql.Literal(data_dict['exp_lifetime']),
        sql.Literal(data_dict['contractor']),
        sql.Literal(data_dict['contractor_country']),
        sql.Literal(data_dict['launch_site']),
        sql.Literal(data_dict['launch_vehicle']),
        sql.Literal(data_dict['cospar']),
        sql.Literal(data_dict['norad']),
        sql.Literal(data_dict['comment_note']),
        sql.Literal(data_dict['source_orbit']),
        sql.Literal(data_dict['source_satellite']),
        sql.Literal(id)
    )
    cur.execute(query)
    # Commit changes to database
    conn.commit()
    # Get ID of updated proposed change
    id = cur.fetchone()[0]
    # Close database connection
    cur.close()
    conn.close()
    if id is None:
        return jsonify({'error': 'Proposed change not found.'}), 404
    # Return ID of updated proposed change
    return jsonify({'id': id}), 200


#approve API
@proposed_changes_subpath.route('/changes/approve/<id>', methods=['PUT'])
def approve_proposed_change(id):
    """
    Request Data:
        - None
    Example Usage:
        PUT /proposed/approve/changes/<id>
    
    Returns:
        - id (str): The ID of the approved proposed change.
    """
    # Connect to PostgreSQL database
    conn = get_db_connection()

    # Create a cursor object
    cur = conn.cursor()
    # Execute SQL query to approve proposed change by ID
    query = sql.SQL("UPDATE proposed_changes SET is_approved = {} WHERE id = {} RETURNING id;").format(
        sql.Literal("approved"),
        sql.Literal(id)
    )
    cur.execute(query)
    # Commit changes to database
    conn.commit()
    # Get ID of approved proposed change
    id = cur.fetchone()[0]
    # Close database connection
    cur.close()
    conn.close()
    if id is None:
        return jsonify({'error': 'Proposed change not found.'}), 404
    # Return ID of approved proposed change
    return jsonify({'id': id}), 200

#deny API
@proposed_changes_subpath.route('/changes/deny/<id>', methods=['PUT'])
def deny_proposed_change(id):
    """
    Request Data:
        - None
    Example Usage:
        PUT /proposed/deny/changes/<id>
    
    Returns:
        - id (str): The ID of the denied proposed change.
    """
    # Connect to PostgreSQL database
    conn = get_db_connection()

    # Create a cursor object
    cur = conn.cursor()
    # Execute SQL query to deny proposed change by ID
    query = sql.SQL("UPDATE proposed_changes SET is_approved = {} WHERE id = {} RETURNING id;").format(
        sql.Literal("denied"),
        sql.Literal(id)
    )
    cur.execute(query)
    # Commit changes to database
    conn.commit()
    # Get ID of denied proposed change
    id = cur.fetchone()[0]
    # Close database connection
    cur.close()
    conn.close()
    if id is None:
        return jsonify({'error': 'Proposed change not found.'}), 404
    # Return ID of denied proposed change
    return jsonify({'id': id}), 200

# Persist save all satellite API: persist and mark all the proposed changes which has been approved as 'persisted', 
# all the proposed changes which has been denied will not be modified, and update the official_satellites table, 
# if the proposed change is neither approve nor denied, leave it in the proposed_changes table.
@proposed_changes_subpath.route('/changes/persist', methods=['POST'])
def save_all_approved_or_denied_changes():
    """
    Request Data:
        - approved_user (str): The user who approved the changes.
    Example Usage:
        POST /proposed/changes/persist
    Returns:
        - message (str): The message confirming the persisted changes.
    """
    # Connect to PostgreSQL database
    conn = get_db_connection()

    # Create a cursor object
    cur = conn.cursor()

    # Execute SQL query to get all approved changes
    query = sql.SQL("SELECT * FROM proposed_changes WHERE is_approved = {};").format(
        sql.Literal("approved")
    )
    cur.execute(query)
    approved_changes = cur.fetchall()

    # Get column names from the cursor description
    colnames = [desc[0] for desc in cur.description]

    if not approved_changes:
        return jsonify({'error': 'No approved changes found.'}), 404

    # Execute SQL query to update is_approved status
    query = sql.SQL("UPDATE proposed_changes SET is_approved = {}, approved_user = {} WHERE is_approved = {};").format(
        sql.Literal("persisted"),
        sql.Literal(request.form['approved_user']),
        sql.Literal("approved")
    )
    cur.execute(query)

    cur.execute("SELECT * FROM official_satellites LIMIT 1;")
    official_satellite_columns = [desc[0] for desc in cur.description]

    # Execute SQL query to update official_satellites table with approved changes and also update the change log
    for row in approved_changes:
        row_dict = dict(zip(colnames, row))

        # Convert launch_date to valid date format
        try:
            if isinstance(row_dict['launch_date'], datetime.date):
                launch_date = row_dict['launch_date']
            else:
                launch_date = datetime.datetime.strptime(row_dict['launch_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': f'Invalid date format for launch_date. Got {row_dict["launch_date"]} ({type(row_dict["launch_date"])})'}), 400

        # Prepare values for official_satellites table
        official_satellite_values = {key: row_dict[key] for key in row_dict if key in official_satellite_columns}
        official_satellite_values['launch_date'] = launch_date

        # Insert into official_satellites table or update on conflict
        cur.execute(f"""
            INSERT INTO official_satellites ({', '.join(official_satellite_values.keys())}) 
            VALUES ({', '.join(['%s'] * len(official_satellite_values))})
            ON CONFLICT (official_name)
            DO UPDATE SET
                {', '.join([f'{key} = excluded.{key}' for key in official_satellite_values.keys()])};
            """, list(official_satellite_values.values())
        )


        # Prepare values for change log
        changelog_values = {
            'update_user': 'admin',
            'update_action': 'persisted',
            'update_time': datetime.datetime.now(),
            'update_notes': 'changes persisted from proposed table',
            **official_satellite_values
        }

        # Insert into change log
        cur.execute(f"""
            INSERT INTO official_satellites_changelog ({', '.join(changelog_values.keys())}) 
            VALUES ({', '.join(['%s'] * len(changelog_values))});
            """, list(changelog_values.values())
        )

    # Commit changes to database
    conn.commit()

    # Close database connection
    cur.close()
    conn.close()

    return jsonify({'message': 'All approved changes have been persisted.'}), 200
