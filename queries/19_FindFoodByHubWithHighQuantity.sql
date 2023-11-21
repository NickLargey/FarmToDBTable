-- Detect food items with high availability at hubs.
-- this query groups the food items associated at each hub together by name AND unit.
-- It returns the SUM of their quantity, the name, and the unit

SELECT fi.fi_name, SUM(fi.fi_quantity) AS total_quantity, fi.fi_unit
FROM FOOD_ITEM fi
JOIN PRODUCER_FOOD_ITEM pfi ON fi.fi_id = pfi.fi_id
JOIN HUB_PRODUCER hp ON pfi.pro_id = hp.pro_id
WHERE hp.hub_id = 2
GROUP BY fi.fi_name, fi.fi_unit;