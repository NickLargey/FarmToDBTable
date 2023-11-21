-- Track a producer's in-progress orders

SELECT po.*
FROM PURCHASE_ORDER po
JOIN FOOD_ITEM fi ON po.pur_fi_id = fi.fi_id
JOIN PRODUCER_FOOD_ITEM pfi ON fi.fi_id = pfi.fi_id
JOIN PRODUCER p ON pfi.pro_id = p.pro_id
WHERE p.pro_id = 2
  AND po.pur_status = 'Ready at Hub';