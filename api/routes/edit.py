from flask import Blueprint, jsonify, request
from utils import get_db_connection

# Create a Blueprint for this subpath
edit_subpath = Blueprint('edit', __name__)

@edit_subpath.route('/create', methods=['POST'])
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


@edit_subpath.route('/update/<int:id>', methods=['PUT'])
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


@edit_subpath.route('/delete/<int:id>', methods=['DELETE'])
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