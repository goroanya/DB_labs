CREATE INDEX treeIndex ON department using btree (id);

ALTER TABLE department
    ADD COLUMN ts_vector tsvector;

UPDATE department
SET ts_vector = to_tsvector(name)
WHERE true;



EXPLAIN
SELECT *
FROM department;


EXPLAIN ANALYSE
SELECT *
FROM department
where id < 100;