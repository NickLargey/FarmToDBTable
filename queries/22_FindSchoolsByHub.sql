-- Identify schools served by a specific hub

SELECT s.*
FROM SCHOOL s
JOIN HUB_SCHOOL hs ON s.sch_id = hs.sch_id
JOIN HUB h ON hs.hub_id = h.hub_id
WHERE h.hub_id = 2;