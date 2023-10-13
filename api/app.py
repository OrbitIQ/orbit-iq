from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)

# Database connection configurations using os.environ
DB_HOST = os.environ.get('DB_HOST', 'db')  # Default to 'db' if not set
DB_PORT = int(os.environ.get('DB_PORT', 5432))  # Default to 5432 if not set
DB_NAME = os.environ.get('POSTGRES_DB', 'mydatabase')  # Default to 'mydatabase' if not set
DB_USER = os.environ.get('POSTGRES_USER', 'user')  # Default to 'user' if not set
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'password')  # Default to 'password' if not set

def get_db_connection():
    """Get a connection to the database."""
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

@app.route('/confirmed/satellites')
def get_satellites():
    """
    Retrieve satellites from the official_satellites table with optional pagination.
    
    URL Parameters:
        - limit (optional): An integer specifying the number of records to return.
            If not provided, all records are returned.
        - page (optional): An integer specifying the page number when using pagination.
            Defaults to 1 if not provided. Used in conjunction with the 'limit' parameter 
            to determine the records offset.

    Example Usage:
        - /confirmed/satellites?limit=10&page=2: Returns records 11-20
        - /confirmed/satellites?limit=5: Returns the first 5 records
        - /confirmed/satellites: Returns all records

    Returns:
        A JSON representation of the selected satellite records.
    """
    
    # Get the optional limit and page parameters from the request URL
    limit = request.args.get('limit', default=None, type=int)
    page = request.args.get('page', default=1, type=int)
    
    # Calculate offset based on limit and page
    offset = (page - 1) * limit if limit else 0

    conn = get_db_connection()
    cursor = conn.cursor()

    # Modify the SQL query to use LIMIT and OFFSET for pagination
    if limit:
        cursor.execute("SELECT * FROM official_satellites LIMIT %s OFFSET %s", (limit, offset))
    else:
        cursor.execute("SELECT * FROM official_satellites")
    
    satellites = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    # Convert the results to a list of dictionaries for JSON serialization
    columns = [desc[0] for desc in cursor.description]
    satellites_as_dict = [dict(zip(columns, row)) for row in satellites]

    return jsonify({'satellites': satellites_as_dict})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)