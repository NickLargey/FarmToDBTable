-- 7. "School Order History: View a school's completed purchase orders for an academic year."

SELECT po.*
FROM PURCHASE_ORDER po
JOIN SCHOOL_PURCHASE_ORDER spo ON po.pur_id = spo.pur_id
JOIN SCHOOL s ON spo.sch_id = s.sch_id
WHERE s.sch_id = 59
  AND po.pur_date BETWEEN '2022-12-31' AND '2023-12-31';