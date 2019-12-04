CREATE OR REPLACE FUNCTION afterUpdateDepartment()
returns trigger
language plpgsql
AS $$
DECLARE
    workers cursor is select * from worker where department_id = NEW.id;
BEGIN
    FOR worker_ IN workers LOOP
        UPDATE worker
        SET position = position || ' at ' || NEW.name || ','
        WHERE id = worker_.id;
    end loop;
    return NEW;
END;
$$;

CREATE TRIGGER insertPosition AFTER UPDATE ON department
    FOR EACH ROW EXECUTE PROCEDURE afterUpdateDepartment();

DROP TRIGGER insertPosition ON department;

UPDATE department SET name='C# Java C++' WHERE id=1;
select * from department;