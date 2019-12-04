CREATE INDEX treeIndex ON department using btree(id);

DROP INDEX treeIndex;

EXPLAIN SELECT * FROM department where id < 100;



alter table department add ts_vector tsvector;
update department set ts_vector = to_tsvector(name);

CREATE INDEX ginIndex ON department using gin(ts_vector);

DROP INDEX ginIndex;

EXPLAIN SELECT * FROM department where to_tsquery('lol') @@ ts_vector;

