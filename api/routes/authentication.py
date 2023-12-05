from flask import Blueprint, jsonify, request
from utils.helpers import get_db_connection
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
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
        query = "INSERT INTO users (username, password_hash, is_admin) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, generate_password_hash(password), True))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"msg": "User created successfully"}), 201
    
    # Lets make sure this user is using a jwt that's valid
    identity = get_jwt_identity()
    if not identity:
        cursor.close()
        conn.close()
        return jsonify({"msg": "This route requires the user to be logged in"}), 401

    # check if user making this request is an admin (priviledged to make other accts)
    query = "SELECT is_admin FROM users WHERE username = %s"
    cursor.execute(query, (identity,))
    res = cursor.fetchone()
    if not res or not res[0]:
        cursor.close()
        conn.close()
        return jsonify({"msg": "User not authorized to create new users"}), 401

    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))

    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"msg": "Username already exists"}), 409
    
    query = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
    cursor.execute(query, (username, generate_password_hash(password)))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"msg": "User created successfully"}), 201

@jwt_required()
@authentication_subpath.route('/delete', methods=['POST'])
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

