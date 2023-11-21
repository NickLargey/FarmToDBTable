-- Identify frequently ordered or available items at hubs.

SELECT fi.fi_name, COUNT(po.pur_id) AS total_purchase_orders
FROM PURCHASE_ORDER po
JOIN FOOD_ITEM fi ON po.pur_fi_id = fi.fi_id
JOIN SCHOOL_PURCHASE_ORDER spo ON po.pur_id = spo.pur_id
JOIN HUB_SCHOOL hs ON spo.sch_id = hs.sch_id
JOIN HUB h ON hs.hub_id = h.hub_id
WHERE h.hub_id = 3
GROUP BY fi.fi_name;