# General Catalog of Artificial Space Objects (GCAT)
#
# URL: https://planet4589.org/space/gcat/
# FILE: https://planet4589.org/space/gcat/tsv/cat/satcat.tsv
#
SOURCE_FILE = "https://planet4589.org/space/gcat/tsv/cat/satcat.tsv"


import pandas as pd
import psycopg2
import json
from psycopg2 import sql
from utils import EnhancedJSONEncoder, get_db_conn
import logging

def gcat():
    df = pd.read_csv(SOURCE_FILE, sep="\t", skiprows=[1])
    df.columns = df.columns.str.strip()

    df = df.replace(["-", " "], [None, None])
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Sort the data by LDate in descending order
    df['LDate'] = pd.to_datetime(df['LDate'], errors='coerce')
    df = df.sort_values(by='LDate', ascending=False)

    conn = get_db_conn()
    cur = conn.cursor()

    # SQL lookup on table sources for name = 'GCAT', to get the right source_id
    cur.execute("SELECT id FROM sources WHERE name = 'GCAT'")
    source_id = cur.fetchone()[0]

    # Hard Cutoff date
    hard_cutoff_date = pd.Timestamp('2023-01-01')

    # Iterate through the sorted data and add new records to the database
    for _, row in df.iterrows():
        # Stop considering satellites launched before Jan 1, 2023
        if row['LDate'] < hard_cutoff_date:
            continue

        external_data_row_id = row['#JCAT']
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