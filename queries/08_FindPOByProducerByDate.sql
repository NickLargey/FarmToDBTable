-- 8. "Producer Order Lookup: Search for a producer's purchase orders by date range."

SELECT po.*
FROM PURCHASE_ORDER po
JOIN FOOD_ITEM fi ON po.pur_fi_id = fi.fi_id
JOIN PRODUCER_FOOD_ITEM pfi ON fi.fi_id = pfi.fi_id
JOIN PRODUCER p ON pfi.pro_id = p.pro_id
WHERE p.pro_id = 1
  AND po.pur_date BETWEEN '2022-12-01' AND '2023-12-31';