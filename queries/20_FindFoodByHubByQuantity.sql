-- Look for food items at a given hub by available quantity

SELECT fi.fi_name, fi.fi_unit, SUM(fi.fi_quantity) AS total_quantity
FROM FOOD_ITEM fi
JOIN PRODUCER_FOOD_ITEM pfi ON fi.fi_id = pfi.fi_id
JOIN HUB_PRODUCER hp ON pfi.pro_id = hp.pro_id
WHERE hp.hub_id = 2
GROUP BY fi.fi_name, fi.fi_unit
HAVING SUM(fi.fi_quantity) > 50;