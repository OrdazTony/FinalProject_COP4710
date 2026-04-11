DROP TRIGGER IF EXISTS mark_pet_unavailable ON AdoptionApplication;
DROP FUNCTION IF EXISTS mark_pet_unavailable_fn();

CREATE OR REPLACE FUNCTION mark_pet_unavailable_fn()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'Approved' THEN
        UPDATE Pet
        SET available = FALSE
        WHERE pet_id = NEW.pet_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER mark_pet_unavailable
AFTER UPDATE ON AdoptionApplication
FOR EACH ROW
EXECUTE FUNCTION mark_pet_unavailable_fn();
