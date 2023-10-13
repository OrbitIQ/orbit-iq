from flask import Flask, jsonify
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
    """Get all satellites from the official_satellites table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
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