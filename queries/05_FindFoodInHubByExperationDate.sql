-- 5.  "Food Expiry Search: Find a hub's food items within a specific expiration date range"

SELECT p.pro_id, p.pro_name, fi.*
FROM HUB_PRODUCER hp
JOIN PRODUCER p ON hp.pro_id = p.pro_id
JOIN PRODUCER_FOOD_ITEM pfi ON p.pro_id = pfi.pro_id
JOIN FOOD_ITEM fi ON pfi.fi_id = fi.fi_id
WHERE hp.hub_id = 3
  AND fi.fi_est_expiration BETWEEN '2023-12-05' AND '2023-12-31';