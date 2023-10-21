from flask import Blueprint, jsonify, request
from utils import get_db_connection

# Create a Blueprint for this subpath
user_subpath = Blueprint('user', __name__)

@user_subpath.route('/get', methods=['GET'])
def get_data():
    """
    Executes a read function , such as SELECT statement on the edit table.
    """
    user_id = request.args.get('userId', default=None)

    if user_id is None:
        return {
            "message": "User ID is required"
        }, 401  
    
    conn = get_db_connection()
    cursor = conn.cursor()

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
    finally:
        cursor.close()
        conn.close()

@user_subpath.route('/create', methods=['POST'])
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
    
    conn = get_db_connection()
    cursor = conn.cursor()

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
    
    finally:
        cursor.close()
        conn.close()
          

@user_subpath.route('/update', methods=['PUT'])
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
    
    conn = get_db_connection()
    cursor = conn.cursor()

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
    
    finally:
        cursor.close()
        conn.close()

@user_subpath.route('/delete', methods=['DELETE'])
def delete_edit():
    """
    Executes a delete function , such as an DELETE statement on the edit table.
    """
    user_id = request.args.get('userId', default = None)

    if user_id is None:
        return {
            "message": "User ID is required"
        }, 422  


    conn = get_db_connection()
    cursor = conn.cursor()

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
    
    finally:
        cursor.close()
        conn.close()


