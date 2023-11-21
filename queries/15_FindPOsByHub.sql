-- Filter a hub's purchase orders by date range.

SELECT po.*
FROM PURCHASE_ORDER po
JOIN SCHOOL_PURCHASE_ORDER spo ON po.pur_id = spo.pur_id
JOIN SCHOOL s ON spo.sch_id = s.sch_id
JOIN HUB_SCHOOL hs ON s.sch_id = hs.sch_id
JOIN HUB h ON hs.hub_id = h.hub_id
WHERE h.hub_id = 1
  AND po.pur_date BETWEEN '2022-12-01' AND '2023-12-31';