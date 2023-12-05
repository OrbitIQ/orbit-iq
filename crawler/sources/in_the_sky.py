# In The Sky Spacecraft Database
#
# We are looking up satellites in our database and trying to fill against 
# the In The Sky Spacecraft Database.
# EX URL: https://in-the-sky.org/spacecraft.php?id=46065

# We are going to recheck each satellite every X days, we are using a modulo for this
# If the norad id of a satellite in our database is divisible
DAYS_UNTIL_RECHECK = 30

import psycopg2
import json
from psycopg2 import sql
from utils import EnhancedJSONEncoder, get_db_conn
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime

base_url = "https://in-the-sky.org/spacecraft.php"

def extract_data(name, norad_id):
    r = requests.get(base_url, params={"id": norad_id})
    if r.status_code != 200:
        return None
    
    # Parse the HTML
    soup = BeautifulSoup(r.text, 'html.parser')
    data = {"official_name": name, "norad": norad_id, "current_date": datetime.now()}

    # Extracting data from the first div
    first_div = soup.find('div', class_='form-item-holder')
    if first_div:
        for row in first_div.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) == 2:
                key = cells[0].get_text(strip=True)
                value = cells[1].get_text(strip=True)
                data[key] = value

    # Extracting data from the subsequent divs
    for div in soup.find_all('div', class_='spacecraft_info_box'):
        table = div.find('table', class_='timeline')
        if table:
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) == 2:
                    key = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True)
                    data[key] = value

    return data

def in_the_sky():
    # add id to the url which is the norad id of the satellite
    conn = get_db_conn()

    cur = conn.cursor()

    # SQL lookup on table sources for name = 'in-the-sky.org', to get the right source_id
    cur.execute("SELECT id FROM sources WHERE name = 'in-the-sky.org'")
    source_id = cur.fetchone()[0]

    # Lets lookup all norad ids from the database
    cur.execute("SELECT official_name, norad FROM official_satellites")

    # get all as a list
    results = cur.fetchall()
    to_check_norad = []
    for i, result in enumerate(results):
        name = result[0]
        norad = result[1]

        if norad % DAYS_UNTIL_RECHECK == datetime.now().day % DAYS_UNTIL_RECHECK:
            to_check_norad.append((name, norad))

    total = len(to_check_norad)
    for i, (name, norad) in enumerate(to_check_norad):
        row = extract_data(name, norad)

        # The external data row id isn't really meant for data sources like this since it's supposed to
        # ensure that we don't add duplicate records. But since we are updating the data for a satellite on
        # a regular basis, we can use the norad id and the current date to ensure that we don't add duplicate
        external_data_row_id = f"norad-{norad}-date-{datetime.now().strftime('%Y-%m-%d')}"

        if row is not None:
            # Update the record
            data = json.dumps(row, cls=EnhancedJSONEncoder)

            # Check if the record already exists
            query = sql.SQL("SELECT 1 FROM crawler_dump WHERE external_data_row_id = %s AND source_id = %s")
            cur.execute(query, (external_data_row_id, source_id))
            if cur.fetchone() is not None:
                continue

            # Insert the new record
            query = sql.SQL("INSERT INTO crawler_dump (source_id, data, external_data_row_id) VALUES (%s, %s, %s)")
            try:
                cur.execute(query, (source_id, data, external_data_row_id))
                conn.commit()
            except psycopg2.IntegrityError as e:
                logging.error(e)
                conn.rollback()

        # Log progress every 100 records
        if i % 100 == 0:
            logging.info(f"In The Sky: Processed {i} of {total} norad ids in this batch (note: we cycle through all norad ids every {DAYS_UNTIL_RECHECK} days)")

    cur.close()
    conn.close()