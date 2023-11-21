-- 9. "Volunteer Role Availability: Find volunteer positions at a hub by day or time"

SELECT r.*
FROM HUB_ROLE hr
JOIN VOLUNTEER_ROLE r ON hr.vrol_id = r.vrol_id
JOIN HUB h ON hr.hub_id = h.hub_id
WHERE h.hub_id = 1;