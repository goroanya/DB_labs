CREATE INDEX treeIndex ON department using btree (id);

EXPLAIN ANALYSE
SELECT *
FROM department
where id < 100;

DROP INDEX treeIndex;


alter table department
    add ts_vector tsvector;
update department
set ts_vector = to_tsvector(name);


CREATE INDEX ginIndex ON department using gin (ts_vector);

EXPLAIN ANALYSE
SELECT *
FROM department
where to_tsquery('c') @@ ts_vector;

DROP INDEX ginIndex;


