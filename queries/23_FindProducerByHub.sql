-- Locate producers connected to a particular hub.

SELECT p.*
FROM PRODUCER p
JOIN HUB_PRODUCER hp ON p.pro_id = hp.pro_id
JOIN HUB h ON hp.hub_id = h.hub_id
WHERE h.hub_id = 2;