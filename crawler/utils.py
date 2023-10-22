import json
import pandas as pd
import os
import psycopg2

# Connect to the PostgreSQL database
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('POSTGRES_DB')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

if any(v is None for v in [DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD]):
    raise Exception("One or more environment variables are missing.")

def get_db_conn():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat() if pd.notna(obj) else None
        elif pd.isna(obj) or obj is pd.NaT:
            return None
        return super(EnhancedJSONEncoder, self).default(obj)