import os
import time
import psycopg2
import logging

from sources.gcat import gcat
from utils import get_db_conn

def setup_sources():
    tries = 0
    while tries < 5:
        try:
            conn = get_db_conn()
            cur = conn.cursor()

            # Now add the sources, lets make sure our IDs are fixed here

            # 1 - GCAT - General Catalog of Artificial Space Objects
            cur.execute("""
                INSERT INTO sources (id, name, url, description) VALUES
                (1, 'GCAT', 'https://planet4589.org/space/gcat/', 'General Catalog of Artificial Space Objects (GCAT)')
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
    logging.info("Starting crawler")
    setup_sources() # create sources table and add sources

    before_count = count_crawler_dump()

    gcat()

    after_count = count_crawler_dump()

    print("Added {} new records to crawler_dump".format(after_count - before_count))

if __name__ == "__main__":
    main()
    print("Done!")