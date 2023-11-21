-- Discover food items that frequently expire at hubs.

SELECT fi.fi_name, COUNT(DISTINCT fi.fi_id) AS total_food_items
FROM FOOD_ITEM fi
JOIN PRODUCER_FOOD_ITEM pfi ON fi.fi_id = pfi.fi_id
JOIN HUB_PRODUCER hp ON pfi.pro_id = hp.pro_id
JOIN HUB h ON hp.hub_id = h.hub_id
JOIN HUB_SCHOOL hs ON h.hub_id = hs.hub_id
JOIN SCHOOL_PURCHASE_ORDER spo ON hs.sch_id = spo.sch_id
WHERE h.hub_id = 2
  AND fi.fi_est_expiration < CURRENT_DATE
GROUP BY fi.fi_name;