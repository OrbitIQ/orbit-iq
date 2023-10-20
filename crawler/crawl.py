import os
import psycopg2
import logging

from sources.gcat import gcat
from utils import get_db_conn

def setup_sources():
    conn = get_db_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sources (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            url VARCHAR(255) NOT NULL UNIQUE,
            description text NOT NULL
        );
    """)

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

def setup_crawler_dump():
    conn = get_db_conn()
    cur = conn.cursor()

    cur.execute("""
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

    conn.commit()
    cur.close()
    conn.close()

def count_crawler_dump():
    conn = get_db_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*) FROM crawler_dump;
    """)

    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return count

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting crawler")
    setup_sources() # create sources table and add sources
    setup_crawler_dump() # create crawler_dump table

    before_count = count_crawler_dump()

    gcat()

    after_count = count_crawler_dump()

    logging.info("Added {} new records to crawler_dump".format(after_count - before_count))

if __name__ == "__main__":
    main()
    print("Done!")