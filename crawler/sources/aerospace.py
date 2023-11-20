# Aerospace Rentry Data

rentry_url = "https://aerospace.org/reentries"

import pandas as pd
import psycopg2
import json
from psycopg2 import sql
from utils import EnhancedJSONEncoder, get_db_conn
import logging
from bs4 import BeautifulSoup
import requests

def aerospace():
    r = requests.get(rentry_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    csv_link = soup.find('a', string='.csv') # this link changes so we need to find it dynamically 
    csv_url = csv_link['href']

    df = pd.read_csv(csv_url, skiprows=[1], low_memory=False)

    # Filter down table to Aerospace Reentry Prediction (UTC) being in the past
    current_time = pd.Timestamp.now(tz='UTC')
    df['Aerospace Reentry Prediction (UTC)'] = pd.to_datetime(df['Aerospace Reentry Prediction (UTC)'], format='ISO8601')
    df = df[df['Aerospace Reentry Prediction (UTC)'] < current_time] # Lets ignore satellites that haven't de-orbited yet

    # df["SSN"] is the satellite catalog number, this is same as norad id
    conn = get_db_conn()
    cur = conn.cursor()

    # SQL lookup on table sources for name = 'Aerospace_reentry', to get the right source_id
    cur.execute("SELECT id FROM sources WHERE name = 'Aerospace_reentry'")
    source_id = cur.fetchone()[0]

    # Conver row['SSN'] to str
    df['SSN'] = df['SSN'].astype(str)

    # filter down type to only "Payload", we only care about this
    df = df[df['Type'] == 'Payload']

    df = df.where(pd.notnull(df), None) # replace NaN with None

    # Convert NaN to None and ensure string columns are handled correctly
    for column in ['Sighting Latitude', 'Sighting Longitude', 'Recovery Latitude', 'Recovery Longitude']:
        df[column] = df[column].astype(str).replace('nan', None)

    # Iterate through the sorted data and add new records to the database
    for _, row in df.iterrows():

        external_data_row_id = row['International Designator'] + row['SSN'] # not sure if SSN is unique so we add the international designator
        data = json.dumps(row.to_dict(), cls=EnhancedJSONEncoder)

        # Check if the record already exists
        query = sql.SQL("SELECT 1 FROM crawler_dump WHERE external_data_row_id = %s AND source_id = %s")
        cur.execute(query, (external_data_row_id, source_id))
        if cur.fetchone() is not None:
            break

        # Insert the new record
        query = sql.SQL("INSERT INTO crawler_dump (source_id, data, external_data_row_id) VALUES (%s, %s, %s)")
        try:
            cur.execute(query, (source_id, data, external_data_row_id))
            conn.commit()
        except psycopg2.IntegrityError as e:
            logging.error(e)
            conn.rollback()

    # Close the connection
    cur.close()
    conn.close()
