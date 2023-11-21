-- Search for a hub's food items by price range and unit type
-- (this sorts the food items available at a hub from cheapest per unit
-- to most expensive per unit, and by unit type

SELECT fi.*
FROM FOOD_ITEM fi
JOIN PRODUCER_FOOD_ITEM pfi ON fi.fi_id = pfi.fi_id
JOIN HUB_PRODUCER hp ON pfi.pro_id = hp.pro_id
WHERE hp.hub_id = 1
ORDER BY fi.fi_cost_per_quantity ASC, fi.fi_unit ASC;