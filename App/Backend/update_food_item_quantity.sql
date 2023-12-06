CREATE OR REPLACE FUNCTION update_food_item_quantity()
RETURNS TRIGGER AS $$
BEGIN
    -- Check if there's enough quantity before attempting update
    IF (SELECT fi_quantity FROM FOOD_ITEM WHERE fi_id = NEW.pur_fi_id) < NEW.pur_quantity THEN
        RAISE EXCEPTION 'Not enough quantity in stock for food item ID: %', NEW.pur_fi_id;
    END IF;

    -- Proceed with updating the food item quantity
    UPDATE FOOD_ITEM
    SET fi_quantity = fi_quantity - NEW.pur_quantity
    WHERE fi_id = NEW.pur_fi_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-- Create a trigger to execute the function after an insert on PURCHASE_ORDER
CREATE TRIGGER after_purchase_order_insert
AFTER INSERT ON PURCHASE_ORDER
FOR EACH ROW
EXECUTE FUNCTION update_food_item_quantity();