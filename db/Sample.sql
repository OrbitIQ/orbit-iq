CREATE TABLE Sample ( date_col VARCHAR(12), mass_col VARCHAR(10) );
COPY Sample2(date_col, mass_col) FROM './SampleData.csv' 
WITH (FORMAT CSV, DELIMITER ',', QUOTE '"');