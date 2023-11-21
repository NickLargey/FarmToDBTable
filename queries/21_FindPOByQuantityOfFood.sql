-- Find purchase orders by the quantity of food ordered

SELECT po.*
FROM PURCHASE_ORDER po
JOIN FOOD_ITEM fi ON po.pur_fi_id = fi.fi_id
WHERE po.pur_status != 'Completed Pickup'
  AND fi.fi_name = 'onions'
  AND fi.fi_unit = 'lb'
  AND po.pur_quantity > 50;