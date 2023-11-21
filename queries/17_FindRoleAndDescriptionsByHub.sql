-- Find volunteer role names and descriptions at specific hubs.

SELECT r.vrol_name, r.vrol_description
FROM HUB_ROLE hr
JOIN ROLE_SLOT r ON hr.vrol_id = r.vrol_id
JOIN HUB h ON hr.hub_id = h.hub_id
WHERE h.hub_id = 2;