from flask import Blueprint, jsonify, request
from utils.helpers import get_db_connection
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, verify_jwt_in_request
from werkzeug.security import generate_password_hash, check_password_hash
import string

# Create a Blueprint for this subpath
authentication_subpath = Blueprint('auth', __name__)

def is_password_secure(password):
    """
    Check if the password is reasonably secure and return reasons if it's not.
    A secure password should have:
    - At least 12 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """
    reasons = []

    if len(password) < 12:
        reasons.append("Password should be at least 12 characters long.")

    if not any(char.isdigit() for char in password):
        reasons.append("Password should include at least one digit.")

    if not any(char.isupper() for char in password):
        reasons.append("Password should include at least one uppercase letter.")

    if not any(char.islower() for char in password):
        reasons.append("Password should include at least one lowercase letter.")

    if not any(char in string.punctuation for char in password):
        reasons.append("Password should include at least one special character.")

    if reasons:
        return False, reasons
    return True, ["Password is secure."]

@authentication_subpath.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    name = request.json.get('name', None)

    if not username or not password:
        return jsonify({"msg": "Username and password required"}), 400
    
    secure, reasons = is_password_secure(password)
    if not secure:
        return jsonify({"msg": "\n".join(reasons)}), 400

    # check if username already exists in table users
    conn = get_db_connection()
    cursor = conn.cursor()

    # check the # of users in the table
    query = "SELECT COUNT(*) FROM users"
    cursor.execute(query)
    count = cursor.fetchone()[0]

    if count == 0:
        # Lets create the first user as an admin and bypass the jwt requirement
        query = "INSERT INTO users (username, name, password_hash, is_admin) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (username, name, generate_password_hash(password), True))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"msg": "User created successfully"}), 201
    
    # Lets make sure this user is using a jwt that's valid
    verify_jwt_in_request()
    identity = get_jwt_identity()
    if not identity:
        cursor.close()
        conn.close()
        return jsonify({"msg": "An admin account already exists, they must create the account for you."}), 401

    # check if user making this request is an admin (priviledged to make other accts)
    query = "SELECT is_admin FROM users WHERE username = %s"
    cursor.execute(query, (identity,))
    res = cursor.fetchone()
    if not res or not res[0]:
        cursor.close()
        conn.close()
        return jsonify({"msg": "User not authorized to create new users."}), 401

    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))

    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"msg": "Username already exists"}), 409
    
    query = "INSERT INTO users (username, name, password_hash) VALUES (%s, %s, %s)"
    cursor.execute(query, (username, name, generate_password_hash(password)))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"msg": "User created successfully"}), 200

@authentication_subpath.route('/delete', methods=['POST'])
@jwt_required()
def delete():
    username = request.json.get('username', None)

    if not username:
        return jsonify({"msg": "Username required"}), 400

    # check if username already exists in table users
    conn = get_db_connection()
    cursor = conn.cursor()

    # check if user making this request is an admin (priviledged to make other accts)
    query = "SELECT is_admin FROM users WHERE username = %s"
    cursor.execute(query, (get_jwt_identity(),))
    res = cursor.fetchone()
    if not res or not res[0]:
        cursor.close()
        conn.close()
        return jsonify({"msg": "User not authorized to delete users"}), 401

    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))

    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"msg": "Username does not exist"}), 404
    
    query = "DELETE FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"msg": "User deleted successfully"}), 200


@authentication_subpath.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    # get user's hashed password from db
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT password_hash FROM users WHERE username = %s"
    cursor.execute(query, (username,))

    user_password = cursor.fetchone()[0]
    if not user_password or not check_password_hash(user_password, password):
        cursor.close()
        conn.close()
        return jsonify({"msg": "Bad username or password"}), 401
    
    cursor.close()
    conn.close()

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@authentication_subpath.route('/edit', methods=['POST'])
@jwt_required()
def edit_user():
    current_user = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the user making the request is an admin
    cursor.execute("SELECT is_admin FROM users WHERE username = %s", (current_user,))
    is_admin = cursor.fetchone()[0]

    if not is_admin:
        cursor.close()
        conn.close()
        return jsonify({"msg": "Only admins can edit user details"}), 403

    # Get request data
    username = request.json.get('username', None)
    new_name = request.json.get('name', None)
    new_username = request.json.get('new_username', None)
    is_admin = request.json.get('is_admin', None)

    if not username:
        return jsonify({"msg": "Username is required"}), 400

    # Check if the user to be edited exists
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"msg": "User not found"}), 404

    # Update user details
    update_query = "UPDATE users SET "
    update_params = []

    if new_name:
        update_query += "name = %s, "
        update_params.append(new_name)

    if new_username:
        update_query += "username = %s, "
        update_params.append(new_username)

    if is_admin is not None:
        update_query += "is_admin = %s, "
        update_params.append(is_admin)

    # Remove trailing comma and space
    update_query = update_query.rstrip(', ')
    update_query += " WHERE username = %s"
    update_params.append(username)

    cursor.execute(update_query, tuple(update_params))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"msg": "User details updated successfully"}), 200

@authentication_subpath.route('/list', methods=['GET'])
@jwt_required()
def list_users():
    # List all users in database: username, full name, is_admin
    current_user = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the user making the request is an admin
    cursor.execute("SELECT is_admin FROM users WHERE username = %s", (current_user,))
    is_admin = cursor.fetchone()[0]
    if not is_admin:
        cursor.close()
        conn.close()
        return jsonify({"msg": "Only admins can list users"}), 403
    
    cursor.execute("SELECT username, name, is_admin FROM users")
    users = cursor.fetchall()

    # Close the connection
    cursor.close()
    conn.close()

    # Convert the results to a list of dictionaries for JSON serialization
    columns = [desc[0] for desc in cursor.description]
    users_as_dict = [dict(zip(columns, row)) for row in users]
    return jsonify({'users': users_as_dict}), 200

@authentication_subpath.route('/isadmin', methods=['GET'])
@jwt_required()
def is_admin():
    current_user = get_jwt_identity()
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if the user making the request is an admin
    cursor.execute("SELECT is_admin FROM users WHERE username = %s", (current_user,))
    is_admin = cursor.fetchone()[0]
    if not is_admin:
        cursor.close()
        conn.close()
        return jsonify({"admin": False}), 200

    cursor.close()
    conn.close()
    return jsonify({"admin": True}), 200