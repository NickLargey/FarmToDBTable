-- reducing the quantity of a food item by providing the
-- food items ID and quantity to reduce it by
-- it checks to make sure the amount doesn't fall below zero

UPDATE FOOD_ITEM
SET fi_quantity =
  CASE
    WHEN fi_quantity - 50 >= 0 THEN fi_quantity - 50
    ELSE 0
  END
WHERE fi_id IN (
    SELECT pfi.fi_id
    FROM PRODUCER_FOOD_ITEM pfi
    JOIN PRODUCER p ON pfi.pro_id = p.pro_id
    WHERE p.pro_id = 2
);