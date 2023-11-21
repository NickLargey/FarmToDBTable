-- Identify a hub's food items by harvest date.
-- this returns all food items harvested AFTER a specific date

SELECT fi.*
FROM FOOD_ITEM fi
JOIN PRODUCER_FOOD_ITEM pfi ON fi.fi_id = pfi.fi_id
JOIN HUB_PRODUCER hp ON pfi.pro_id = hp.pro_id
WHERE hp.hub_id = 2
  AND fi.fi_date_harvested > '2023-12-01';