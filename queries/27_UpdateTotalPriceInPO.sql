-- Update the pur_total_price in the PURCHASE_ORDER table

UPDATE PURCHASE_ORDER
SET pur_total_price = pur_quantity * fi_cost_per_quantity
FROM FOOD_ITEM
WHERE PURCHASE_ORDER.pur_fi_id = FOOD_ITEM.fi_id;