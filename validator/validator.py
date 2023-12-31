from psycopg2 import extras
from proposed_change import ProposedChange, insert_proposed_change
from utils.helpers import get_db_connection
from mappings.gcat import from_gcat
from mappings.aerospace import from_aerospace
from mappings.in_the_sky import from_in_the_sky
from typing import Optional
import time
import logging

source_id_to_mapper = {
    1: from_gcat,
    2: from_aerospace,
    3: from_in_the_sky
}

# Needs to pull from crawler_dump table
# Ignore records that have a proposed change already
def crawler_dump(conn=None):
    if conn is None:
        conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=extras.DictCursor)
    sql = """
        SELECT crawler_dump.* FROM crawler_dump
        LEFT JOIN crawler_dump_proposed_changes
        ON crawler_dump.id = crawler_dump_proposed_changes.crawler_dump_id
        WHERE crawler_dump_proposed_changes.crawler_dump_id IS NULL
    """
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return results


# Need to consider the source it came from and map the fields to a
# single object/format of proposed_changes columns
def map_to_proposed_change(record) -> Optional[ProposedChange]:
    source_id = record['source_id']
    mapper = source_id_to_mapper[source_id]
    return mapper(record)

# Send it to the proposed_changes table
if __name__ == "__main__":
    time.sleep(60) 
    
    HOURS_SLEEP = 24
    logging.basicConfig(level=logging.INFO)

    while True:
        try:
            logging.info("Starting validator")

            conn = get_db_connection()
            records = crawler_dump(conn=conn)

            for record in records:
                proposed_change = map_to_proposed_change(record)

                # TODO: When we get multiple sources we will need to try to combine the proposed changes together into one object then put it in insert_proposed_change
                if proposed_change is not None:
                    insert_proposed_change(proposed_change, [record['id']])

            conn.close()

            logging.info(f"Validator waiting for {HOURS_SLEEP} hours")
        except Exception as e:
            logging.getLogger().error(e)
            logging.getLogger().error("Validator failed")

        time.sleep(HOURS_SLEEP * 60 * 60)