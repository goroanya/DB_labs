CREATE OR REPLACE FUNCTION afterUpdateDepartment()
returns trigger
language plpgsql
AS $$
DECLARE
    workers cursor is select id from worker where department_id = NEW.id;
BEGIN
    FOR wprker IN workers LOOP
        UPDATE worker
        SET position = position || ' at ' || NEW.name
        WHERE id = worker.id;
    end loop;
    return NEW;
END;
$$;

DROP TRIGGER rename ON department;

CREATE TRIGGER rename AFTER UPDATE ON department
    FOR EACH ROW EXECUTE PROCEDURE afterUpdateDepartment();

UPDATE department SET name='new AAA' WHERE id=1;
select * from worker;