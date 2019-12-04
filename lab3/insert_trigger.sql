CREATE OR REPLACE FUNCTION afterAddWorker()
returns trigger
language plpgsql
AS $$
BEGIN
    IF NEW.age > 30  THEN
        UPDATE department SET name=name || ' old' WHERE id = NEW.department_id;
    ELSE
        UPDATE department SET name=name || ' young' WHERE id = NEW.department_id;
    END IF;
    return NEW;
END;
$$;

DROP TRIGGER rename on worker;

CREATE TRIGGER rename AFTER INSERT ON worker
    FOR EACH ROW EXECUTE PROCEDURE afterAddWorker();

INSERT INTO worker( full_name, age, position, department_id)
VALUES ('AAA', 1, 'loh', 1);

