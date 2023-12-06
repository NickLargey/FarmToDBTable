CREATE OR REPLACE FUNCTION add_school_to_hub()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO HUB_SCHOOL (hub_id, sch_id)
    SELECT H.hub_id, NEW.sch_id
    FROM HUB H
    WHERE H.hub_county = NEW.sch_county;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_add_school_to_hub
AFTER INSERT ON SCHOOL
FOR EACH ROW
EXECUTE FUNCTION add_school_to_hub();
