from flask import Flask, request
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

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

conn = get_db_connection()
cursor = conn.cursor()

@app.route('/get', methods=['GET'])
def get_data():
    """
    Executes a read function , such as SELECT statement on the edit table.
    """
    user_id = request.args.get('userId', default=None)

    if user_id is None:
        return {
            "message": "User ID is required"
        }, 401  

    try:
        cursor.execute("SELECT * FROM edit WHERE user_id = %s", (user_id,))
        user_data = cursor.fetchall()
    
        if user_data:
            return {
                "message": "Data returned successfully",
                "edit": user_data
            }, 200
        else:
            return {
                "message": "Edit not found."
             }, 404

    except Exception as e:
        return {
            "error": str(e),
             "message": "An internal server error occurred. Please contact admin."
             }, 500

@app.route('/create', methods=['POST'])
def create_edit():
    """
    Executes a creat function , such as an INSERT INTO statement on the edit table.
    """
    new_data = request.get_json()
    if new_data is None or "userId" not in new_data:
        return {
            "statusCode": 400,
            "error": "Bad request", 
            "message": "Invalid input format."
        }, 400

    user_id = new_data["userId"]
    edit_data = new_data["edit_data"]  
    if user_id is None:
        return {
            "message": "User ID is required"
        }, 422 

    try:
        cursor.execute(
            cursor.execute("SELECT * FROM edit WHERE user_id = %s", (user_id,))
            )

        existing_edit = cursor.fetchone()
        if existing_edit:
            return {
                "error": "Conflict",
                "message": "Edit already made"
            }, 409  

        cursor.execute("INSERT INTO edit (user_id, edit_data) VALUES (%s, %s)", (user_id, edit_data))
        conn.commit()   

        return{
            "message": "Edit created successfully."
        }, 210
        
    except Exception as e:
        return {
            "error": str(e),
             "message": "An internal server error occurred. Please contact admin."
        }, 500
          

@app.route('/update', methods=['PUT'])
def update_edit():
    """
    Executes a update function , such as an UPDATE statement on the edit table.
    """
    new_data = request.get_json()

    if new_data is None or "userId" not in new_data or "edit_data" not in new_data:
        return {
            "statusCode": 400, 
            "error": "Bad request", 
            "message": "Invalid input format."
        }, 400

    user_id = new_data["userId"]
    edit_data = new_data["edit_data"]
    if user_id is None:
        return {
            "message": "User ID is required"
        }, 422 

    try:
        cursor.execute("UPDATE edit SET edit_data = %s WHERE user_id = %s", (edit_data, user_id))
        conn.commit()

        return {
            "message": "Edit updated successfully"
        }, 204 

    except Exception as e:
        return {
            "message": "An internal server error occurred. Please contact admin.",
            "error": str(e)
        }, 500 

@app.route('/delete>', methods=['DELETE'])
def delete_edit():
    """
    Executes a delete function , such as an DELETE statement on the edit table.
    """
    user_id = request.args.get('userId', default = None)

    if user_id is None:
        return {
            "message": "User ID is required"
        }, 422  

    try:
        cursor.execute("DELETE FROM edit WHERE user_id = %s", (user_id,))
        conn.commit()

        return {
            "message": "Edit deleted successfully"
        }, 204  

    except Exception as e:
        return {
            "message": "An internal server error occurred. Please contact admin.",
            "error": str(e)
        }, 500  


