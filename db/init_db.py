import os
import psycopg2
import csv
from datetime import datetime
import time

# Read from environment variables
DB_NAME = os.environ.get('POSTGRES_DB')
DB_USER = os.environ.get('POSTGRES_USER')
DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')

if any(v is None for v in [DB_NAME, DB_USER, DB_PASSWORD, DB_HOST]):
    raise Exception("One or more environment variables are missing.")

# Connect to PostgreSQL
tries = 0
conn = None
while tries < 5:
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
        )
    except psycopg2.OperationalError:
        # assume this just failed bc db is still starting up
        pass

    if conn is not None:
        break

    tries += 1
    time.sleep(5)

    
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
    detailed_purpose text,
    orbit_class VARCHAR(255), 
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
    launch_date DATE,
    exp_lifetime VARCHAR(255),
    contractor VARCHAR(255),
    contractor_country VARCHAR(255),
    launch_site VARCHAR(255),
    launch_vehicle VARCHAR(255),
    cospar  VARCHAR(20),
    norad integer,
    comment_note text,
    source_orbit text,
    source_satellite text[]
);
""")

# Create changelog table
cursor.execute("""
CREATE TABLE IF NOT EXISTS official_satellites_changelog ( 
    cid UUID PRIMARY KEY,
    update_user VARCHAR(255),
    update_action VARCHAR(10),
    update_time DATE,
    update_notes text,
    official_name VARCHAR(255) REFERENCES official_satellites(official_name),
    reg_country VARCHAR(255),
    own_country VARCHAR(255),
    owner_name VARCHAR(255),
    user_type VARCHAR(255),
    purposes VARCHAR(255),
    detailed_purpose text,
    orbit_class VARCHAR(255), 
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
    launch_date DATE,
    exp_lifetime VARCHAR(255),
    contractor VARCHAR(255),
    contractor_country VARCHAR(255),
    launch_site VARCHAR(255),
    launch_vehicle VARCHAR(255),
    cospar  VARCHAR(20),
    norad integer,
    comment_note text,
    source_orbit text,
    source_satellite text[]
);
""")

# Create proposed_changes table
# TODO: @stevenlai1688 to finish up schema
# David - I added this bc I needed it for schema change
cursor.execute("""
CREATE TABLE IF NOT EXISTS proposed_changes ( 
    id UUID PRIMARY KEY,
    official_name VARCHAR(255)
);
""")

# TODO: DANGER DANGER DANGER
cursor.execute("""
    DROP TABLE IF EXISTS crawler_dump CASCADE;
""")

# Set up the crawler dump table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS crawler_dump (
        id SERIAL PRIMARY KEY,
        external_data_row_id text, /* this is the id that the source uses to identify the row that it scraped */
        source_id INTEGER REFERENCES sources(id),
        data JSONB NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        UNIQUE (external_data_row_id, source_id)
    );
""")             

# I want to map what crawler dumps went into creating a proposed change
# I cannot do a 1:many on proposed_changes bc of psql limitation on array for foreign key constraints isn't allowed
# so we make a mapping table.
cursor.execute("""
CREATE TABLE IF NOT EXISTS crawler_dump_proposed_changes (
    crawler_dump_id SERIAL REFERENCES crawler_dump(id),
    proposed_change_id UUID REFERENCES proposed_changes(id),
    PRIMARY KEY (crawler_dump_id, proposed_change_id)
);""")

# Create an index bc the validator wants to (mostly) ignore records that already have been
# used in a crawler dump
cursor.execute("""
CREATE INDEX IF NOT EXISTS idx_crawler_dump_id
ON crawler_dump_proposed_changes (crawler_dump_id);
""")

# Should probably first check that the table is empty before inserting, or was just created above.
cursor.execute("SELECT COUNT(*) FROM official_satellites")
count = cursor.fetchone()[0]
    
if count == 0:
    # Path to the CSV file
    csv_file = "UCS-Satellite-Database-Officialname-1-1-2023.csv"

    #log info
    print("Reading from CSV file: " + csv_file)
    # Open and read the CSV file
    with open(csv_file, 'r') as file:
        
        csv_reader = csv.reader(file)
        headers = next(csv_reader)
        launch_date_index = headers.index('Date of Launch')
        print("Inserting data into the database...")
        
        for row in csv_reader:
            # Replace empty strings with None in the row
            row = [None if val == "" else val for val in row]
            # Convert the source_satellite column to a list of strings
            source_satellite = row[28:]

            launch_date = row[launch_date_index]

            # manual fixes
            if launch_date == "11/29/018":
                launch_date = "2018/11/29"

            if launch_date:
                try:
                    # Convert the string to a date object
                    date_object = datetime.strptime(launch_date, '%Y/%m/%d')
                    # Convert the date object back to a string in 'YYYY-MM-DD' format
                    launch_date = date_object.strftime('%Y-%m-%d')
                except ValueError:
                    print(f"Error converting launch date '{launch_date}' to date format. Using None.")
                    launch_date = None
            row[launch_date_index] = launch_date

            # Replace empty strings with None in the row
            row = [None if val == "" else val for val in row]
            # Convert the source_satellite column to a list of strings
        
            cursor.execute("""
            INSERT INTO official_satellites (official_name, reg_country, own_country, owner_name, user_type, purposes, detailed_purpose, orbit_class, orbit_type, geo_longitude, perigee, apogee, eccentricity, inclination, period_min, mass_launch, mass_dry, power_watts, launch_date, exp_lifetime, contractor, contractor_country, launch_site, launch_vehicle, cospar, norad, comment_note, source_orbit, source_satellite) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, row[:28] + [source_satellite])
    
print("Data inserted successfully!")

# Commit changes and close connection
conn.commit()
cursor.close()
conn.close()
