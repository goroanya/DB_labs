ALTER TABLE department
    ADD COLUMN ts_vector tsvector;

UPDATE department
SET ts_vector = to_tsvector(name)
WHERE true;

CREATE INDEX ginIndex ON department USING gin (ts_vector);

EXPLAIN
SELECT *
FROM department
WHERE to_tsquery('c') @@ ts_vector;

SELECT *
FROM department;