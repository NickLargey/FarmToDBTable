CREATE OR REPLACE FUNCTION add_producer_to_hub()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO HUB_PRODUCER (hub_id, pro_id)
    SELECT H.hub_id, NEW.pro_id
    FROM HUB H
    WHERE H.hub_county = NEW.pro_county;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_add_producer_to_hub
AFTER INSERT ON PRODUCER
FOR EACH ROW
EXECUTE FUNCTION add_producer_to_hub();
