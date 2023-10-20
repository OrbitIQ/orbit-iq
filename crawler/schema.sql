CREATE TABLE sources (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    url VARCHAR(255) NOT NULL UNIQUE,
    description text NOT NULL
);

CREATE TABLE crawler_dump (
    id SERIAL PRIMARY KEY,
    external_data_row_id text, /* this is the id that the source uses to identify the row that it scraped */
    source_id INTEGER REFERENCES source(id),
    data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (external_data_row_id, source_id)
);