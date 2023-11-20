import psycopg2
import os

# Database connection configurations using os.environ
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

def get_proposed_changes_columns():
    """
    Fetch the column names of the proposed_changes table.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'proposed_changes'")
            columns = [row[0] for row in cursor.fetchall()]
    return columns

def validate_norad(norad):
    """
    Validate a NORAD ID.
    - NORAD ID should be a non-empty value.
    - NORAD ID should be a number (if it's a string, it should contain only digits).
    - NORAD ID should have exactly 5 digits.
    """
    # if string input convert to int if possible
    if isinstance(norad, str):
        try:
            norad = int(norad)
        except ValueError:
            return False
        
    
    if not norad:
        return False
    
    if not isinstance(norad, int):
        return False
    
    if 1 <= norad <= 999999999:
        return True
    
    return False

def get_key(data, key, default=None):
    """
    Get a key from a dictionary, returning a default value if the key is not present.
    """
    r = data.get(key, default)
    if r is None:
        return default
    return r