-- 6. "List Suppliers by Product: Identify producers that supply particular food items."

SELECT DISTINCT p.pro_id, p.pro_name
FROM PRODUCER p
JOIN PRODUCER_FOOD_ITEM pfi ON p.pro_id = pfi.pro_id
JOIN FOOD_ITEM fi ON pfi.fi_id = fi.fi_id
WHERE fi.fi_name = 'eggs';