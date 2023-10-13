import os
import psycopg2

# Read from environment variables
DB_NAME = os.environ.get('POSTGRES_DB')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_HOST = os.environ.get('DB_HOST', 'db')  # Default to 'db' if not specified

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST
)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS official_satellites ( 
    official_name VARCHAR(255) PRIMARY KEY,
    reg_country VARCHAR(255),
    own_country VARCHAR(255),
    owner_name VARCHAR(255),
    user_type VARCHAR(255),
    purposes VARCHAR(255),
    orbit_class VARCHAR(16), 
    orbit_type VARCHAR(255),
    geo_longitude VARCHAR(255),
    perigee VARCHAR(255),
    apogee VARCHAR(255),
    eccentricity VARCHAR(255),
    inclination VARCHAR(255),
    period_min VARCHAR(255),
    mass_launch VARCHAR(255),
    mass_dry VARCHAR(255),
    power_watts VARCHAR(255),
    launch_date VARCHAR(255),
    exp_lifetime VARCHAR(255),
    contractor VARCHAR(255),
    contractor_country VARCHAR(255),
    launch_site VARCHAR(255),
    launch_vehicle VARCHAR(255),
    cospar_number  VARCHAR(20),
    norad_number integer,
    comment_note VARCHAR(255),
    source_orbit VARCHAR(255),
    source_satellite text[]
    );
""")

# Should probably first check that the table is empty before inserting, or was just created above.

conn.commit()
cursor.close()
conn.close()
