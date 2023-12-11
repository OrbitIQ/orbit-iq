import os
import time
import psycopg2
import logging

from sources.gcat import gcat
from sources.aerospace import aerospace
from sources.in_the_sky import in_the_sky
from utils import get_db_conn

def setup_sources():
    tries = 0
    while tries < 5:
        try:
            conn = get_db_conn()
            cur = conn.cursor()

            # Now add the sources, lets make sure our IDs are fixed here

            # 1 - GCAT - General Catalog of Artificial Space Objects
            # 2 - Aerospace_reentry - Aerospace Reentry Data
            # 3 - In The Sky - in-the-sky.org
            cur.execute("""
                INSERT INTO sources (id, name, url, description) VALUES
                (1, 'GCAT', 'https://planet4589.org/space/gcat/', 'General Catalog of Artificial Space Objects (GCAT)'),
                (2, 'Aerospace_reentry', 'https://aerospace.org/reentries', 'Aerospace Reentry Data'),
                (3, 'in-the-sky.org', 'https://in-the-sky.org/spacecraft.php', 'in-the-sky.org')
                ON CONFLICT DO NOTHING;
            """)
        
            conn.commit()
            cur.close()
            conn.close()
            return
        except psycopg2.errors.UndefinedTable:
            time.sleep(5)
            tries += 1


def count_crawler_dump():
    conn = get_db_conn()
    cur = conn.cursor()

    tries = 0
    count = 0
    while tries < 5:
        try:
            cur.execute("""
                SELECT COUNT(*) FROM crawler_dump;
            """)
            count = cur.fetchone()[0]
            break
        except psycopg2.errors.UndefinedTable:
            # wait for table to be created if it doesn't exist yet
            conn.rollback()  # rollback the transaction
            time.sleep(3)
        except Exception as e:
            logging.error(f"Failed to count crawler_dump: {e}")
            break
        finally:
            tries += 1

    cur.close()
    conn.close()

    return count


def main():
    logging.basicConfig(level=logging.INFO)

    while True:
        logging.info("Starting crawler")
        setup_sources() # create sources table and add sources

        start_count = count_crawler_dump()

        gcat()

        after_gcat_count = count_crawler_dump()

        aerospace()

        after_aerospace_count = count_crawler_dump()

        print("We are now going to crawl in-the-sky.org, this will take a while")
        in_the_sky() # this one is slow so we do it last

        after_count = count_crawler_dump()

        print(f"Added {after_count - start_count} new records to crawler_dump")
        print(f"\tGCAT: {after_gcat_count - start_count}")
        print(f"\tAerospace Reentry: {after_aerospace_count - after_gcat_count}")
        print(f"\tin-the-sky.org: {after_count - after_aerospace_count}")

        SLEEP_HOURS = 24
        print(f"Sleeping for {SLEEP_HOURS} hours")
        time.sleep(SLEEP_HOURS * 60 * 60)

if __name__ == "__main__":
    main()
    print("Done!")