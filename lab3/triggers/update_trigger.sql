CREATE OR REPLACE FUNCTION afterUpdateDepartment()
    returns trigger
    language plpgsql
AS
$$
DECLARE
    workers cursor is select *
                      from worker
                      where department_id = NEW.id;
BEGIN
    FOR _worker IN workers
        LOOP
            UPDATE worker
            SET position = position || ' at ' || NEW.name || ','

            WHERE id = _worker.id;
        end loop;
    return NEW;
END ;
$$;

CREATE TRIGGER insertPosition
    AFTER UPDATE
    ON department
    FOR EACH ROW
EXECUTE PROCEDURE afterUpdateDepartment();

DROP TRIGGER insertPosition ON department;


select *
from worker;

update department
set name = 'C#'
where id = 1;




