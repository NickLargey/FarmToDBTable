-- 4. "Check Food Type Availability: Search a hub's inventory for future availability by macro
-- (e.g., vegetable, fruit, protein)."

-- 4a. just all the food "at" a hub

SELECT p.pro_id, p.pro_name, fi.*
FROM HUB_PRODUCER hp
JOIN PRODUCER p ON hp.pro_id = p.pro_id
JOIN PRODUCER_FOOD_ITEM pfi ON p.pro_id = pfi.pro_id
JOIN FOOD_ITEM fi ON pfi.fi_id = fi.fi_id
WHERE hp.hub_id = 1
  AND fi.fi_est_expiration > CURRENT_DATE;