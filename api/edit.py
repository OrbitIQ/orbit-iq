from flask import Flask, request, jsonify, redirect, url_for, flash
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
    return response

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('POSTGRES_DB')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

if any(v is None for v in [DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD]):
    raise Exception("One or more environment variables are missing.")

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

@app.route('/confirmed/satellites', methods=["GET"])
def read():
    """
    Executes a read function , such as SELECT statement on the edit table.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Execute a SELECT query to retrieve data from the official_satellites table
    cursor.execute("SELECT * FROM official_satellites")
    records = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return jsonify({'satellites': records})
   

@app.route('/create', methods=['POST'])
def create():
    """
    Executes a creat function , such as an INSERT INTO statement on the edit table.
    """
    if request.method == 'POST':
        data = request.form['data']
        source = request.form['source']

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert a new record into the official_satellites table
        insert_query = "INSERT INTO official_satellites (data, source) VALUES (%s, %s)"
        cursor.execute(insert_query, (data, source))
        conn.commit()

        cursor.close()
        conn.close()


@app.route('/update/<int:id>', methods=['PUT'])
def update(id):
    """
    Executes a update function , such as an UPDATE statement on the edit table.
    """
    if request.method == 'PUT':
        data = request.form['data']
        source = request.form['source']

        conn = get_db_connection()
        cursor = conn.cursor()

        update_query = "UPDATE official_satellites SET data = %s, source = %s WHERE id = %s"
        cursor.execute(update_query, (data, source, id))
        conn.commit()

        cursor.close()
        conn.close()


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    """
    Executes a delete function , such as an DELETE statement on the edit table.
    """
    if request.method == 'DELETE':
        conn = get_db_connection()
        cursor = conn.cursor()

        delete_query = "DELETE FROM official_satellites WHERE id = %s"
        cursor.execute(delete_query, (id,))
        conn.commit()

        cursor.close()
        conn.close()

