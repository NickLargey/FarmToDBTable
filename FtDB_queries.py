"""

--THE 25 (plus 2)

1.
-- Find hubs based on county
SELECT *
FROM HUB
WHERE hub_county = 'Cumberland'



2.
-- Find producers based on county
SELECT *
FROM PRODUCER
WHERE pro_county = 'Cumberland'



3.
-- Find schools based on county
SELECT *
FROM SCHOOL
WHERE sch_county = 'Cumberland';



4. "Check Food Type Availability: Search a hub's inventory for future availability by macro
(e.g., vegetable, fruit, protein)."

4a. (just all the food "at" a hub)

SELECT p.pro_id, p.pro_name, fi.*
FROM HUB_PRODUCER hp
JOIN PRODUCER p ON hp.pro_id = p.pro_id
JOIN PRODUCER_FOOD_ITEM pfi ON p.pro_id = pfi.pro_id
JOIN FOOD_ITEM fi ON pfi.fi_id = fi.fi_id
WHERE hp.hub_id = 1
  AND fi.fi_est_expiration > CURRENT_DATE;

4b. (all the food by macro "at" a hub)

SELECT p.pro_id, p.pro_name, fi.*
FROM HUB_PRODUCER hp
JOIN PRODUCER p ON hp.pro_id = p.pro_id
JOIN PRODUCER_FOOD_ITEM pfi ON p.pro_id = pfi.pro_id
JOIN FOOD_ITEM fi ON pfi.fi_id = fi.fi_id
WHERE hp.hub_id = 2
  AND fi.fi_macro = 'Vegetables';



5.  "Food Expiry Search: Find a hub's food items within a specific expiration date range"

SELECT p.pro_id, p.pro_name, fi.*
FROM HUB_PRODUCER hp
JOIN PRODUCER p ON hp.pro_id = p.pro_id
JOIN PRODUCER_FOOD_ITEM pfi ON p.pro_id = pfi.pro_id
JOIN FOOD_ITEM fi ON pfi.fi_id = fi.fi_id
WHERE hp.hub_id = 3
  AND fi.fi_est_expiration BETWEEN '2023-12-05' AND '2023-12-31';



6. "List Suppliers by Product: Identify producers that supply particular food items."

SELECT DISTINCT p.pro_id, p.pro_name
FROM PRODUCER p
JOIN PRODUCER_FOOD_ITEM pfi ON p.pro_id = pfi.pro_id
JOIN FOOD_ITEM fi ON pfi.fi_id = fi.fi_id
WHERE fi.fi_name = 'eggs';



7. "School Order History: View a school's completed purchase orders for an academic year."

SELECT po.*
FROM PURCHASE_ORDER po
JOIN SCHOOL_PURCHASE_ORDER spo ON po.pur_id = spo.pur_id
JOIN SCHOOL s ON spo.sch_id = s.sch_id
WHERE s.sch_id = 59
  AND po.pur_date BETWEEN '2022-12-31' AND '2023-12-31';


8. "Producer Order Lookup: Search for a producer's purchase orders by date range."

SELECT po.*
FROM PURCHASE_ORDER po
JOIN FOOD_ITEM fi ON po.pur_fi_id = fi.fi_id
JOIN PRODUCER_FOOD_ITEM pfi ON fi.fi_id = pfi.fi_id
JOIN PRODUCER p ON pfi.pro_id = p.pro_id
WHERE p.pro_id = 1
  AND po.pur_date BETWEEN '2022-12-01' AND '2023-12-31';


9. "Volunteer Role Availability: Find volunteer positions at a hub by day or time"
9a. (all volunteer roles at any given hub)

SELECT r.*
FROM HUB_ROLE hr
JOIN VOLUNTEER_ROLE r ON hr.vrol_id = r.vrol_id
JOIN HUB h ON hr.hub_id = h.hub_id
WHERE h.hub_id = 1;

9b. (all "open" volunteer roles at any given hub (not in the volunteer_role table, meaning on volunteer has fullfilled it yet))

SELECT r.*
FROM HUB_ROLE hr
JOIN VOLUNTEER_ROLE r ON hr.vrol_id = r.vrol_id
JOIN HUB h ON hr.hub_id = h.hub_id
LEFT JOIN VOLUNTEER_ROLE vr ON hr.vrol_id = vr.vrol_id
WHERE h.hub_id = <your_hub_id> AND vr.vrol_id IS NULL;



10. "Volunteer Directory: Retrieve volunteer phone numbers by name."

SELECT vol_phone
FROM VOLUNTEER
WHERE vol_name = 'Aimee Franklin';


11.  "Hub Schedule Info: Access a hub's operating hours by its name."

SELECT hub_hours
FROM HUB
WHERE hub_name = 'Cumberland Hub';



12. "Producer Contact Info: Look up producer email addresses by name."

SELECT pro_email
FROM PRODUCER
WHERE pro_name = 'Duff Farms';



13. "School Address Finder: Get the address of a school by its name"

SELECT sch_address
FROM SCHOOL
WHERE sch_name = 'Deering High School';



14. "Hub Food Pricing: Search for a hub's food items by price range and unit type"
(this sorts the food items avaiable at a hub from cheapest per ubnit to most expensive per unit, and by unit type)

SELECT fi.*
FROM FOOD_ITEM fi
JOIN PRODUCER_FOOD_ITEM pfi ON fi.fi_id = pfi.fi_id
JOIN HUB_PRODUCER hp ON pfi.pro_id = hp.pro_id
WHERE hp.hub_id = <your_hub_id>
ORDER BY fi.fi_cost_per_quantity ASC, fi.fi_unit ASC;



15 "Hub Order Timeline: Filter a hub's purchase orders by date range."

SELECT po.*
FROM PURCHASE_ORDER po
JOIN SCHOOL_PURCHASE_ORDER spo ON po.pur_id = spo.pur_id
JOIN SCHOOL s ON spo.sch_id = s.sch_id
JOIN HUB_SCHOOL hs ON s.sch_id = hs.sch_id
JOIN HUB h ON hs.hub_id = h.hub_id
WHERE h.hub_id = <your_hub_id>
  AND po.pur_date BETWEEN '<start_date>' AND '<end_date>';



16. "Producer's Current Orders: Track a producer's in-progress orders"

  SELECT po.*
  FROM PURCHASE_ORDER po
  JOIN FOOD_ITEM fi ON po.pur_fi_id = fi.fi_id
  JOIN PRODUCER_FOOD_ITEM pfi ON fi.fi_id = pfi.fi_id
  JOIN PRODUCER p ON pfi.pro_id = p.pro_id
  WHERE p.pro_id = <your_producer_id>
    AND po.pur_status = 'Ready at Hub'::order_status_enum;



17. "Hub Volunteer Matching: Find volunteer role names and descriptions at specific hubs."

SELECT r.vrol_name, r.vrol_description
FROM HUB_ROLE hr
JOIN ROLE_SLOT r ON hr.vrol_id = r.vrol_id
JOIN HUB h ON hr.hub_id = h.hub_id
WHERE h.hub_id = <your_hub_id>;



18. "Harvest Date Lookup: Identify a hub's food items by harvest date."
(this returns all food items harvested AFRTER a specifc date)

SELECT fi.*
FROM FOOD_ITEM fi
JOIN PRODUCER_FOOD_ITEM pfi ON fi.fi_id = pfi.fi_id
JOIN HUB_PRODUCER hp ON pfi.pro_id = hp.pro_id
WHERE hp.hub_id = <your_hub_id>
  AND fi.fi_date_harvested > '<your_specific_date>';



19. "Food Surplus Identification: Detect food items with high availability at hubs."
(this query groups the food items associated at each hub together by name AND unit.
It returns the SUM of their quantity, the name, and the unit)

SELECT fi.fi_name, SUM(fi.fi_quantity) AS total_quantity, fi.fi_unit
FROM FOOD_ITEM fi
JOIN PRODUCER_FOOD_ITEM pfi ON fi.fi_id = pfi.fi_id
JOIN HUB_PRODUCER hp ON pfi.pro_id = hp.pro_id
WHERE hp.hub_id = <your_hub_id>
GROUP BY fi.fi_name, fi.fi_unit;



20. "Food Quantity Search: Look for food items at a given hub by available quantity"

SELECT fi.fi_name, fi.fi_unit, SUM(fi.fi_quantity) AS total_quantity
FROM FOOD_ITEM fi
JOIN PRODUCER_FOOD_ITEM pfi ON fi.fi_id = pfi.fi_id
JOIN HUB_PRODUCER hp ON pfi.pro_id = hp.pro_id
WHERE hp.hub_id = <your_hub_id>
GROUP BY fi.fi_name, fi.fi_unit
HAVING SUM(fi.fi_quantity) > <your_specific_amount>;



21. "Order Quantity Analysis: Find purchase orders by the quantity of food ordered"

SELECT po.*
FROM PURCHASE_ORDER po
JOIN FOOD_ITEM fi ON po.fi_id = fi.fi_id
WHERE po.pur_status = 3
  AND fi.fi_name = '<your_food_item_name>'
  AND fi.fi_unit = '<your_food_item_unit>'
  AND po.pur_quantity > <your_min_quantity>;



22. "School-Hub Connection: Identify schools served by a specific hub"

SELECT s.*
FROM SCHOOL s
JOIN HUB_SCHOOL hs ON s.sch_id = hs.sch_id
JOIN HUB h ON hs.hub_id = h.hub_id
WHERE h.hub_id = <your_hub_id>;



23. "Producer-Hub Affiliation: Locate producers connected to a particular hub."

SELECT p.*
FROM PRODUCER p
JOIN HUB_PRODUCER hp ON p.pro_id = hp.pro_id
JOIN HUB h ON hp.hub_id = h.hub_id
WHERE h.hub_id = <your_hub_id>;



24. "Popular Food Tracking: Identify frequently ordered or available items at hubs."

SELECT fi.fi_name, COUNT(po.pur_id) AS total_purchase_orders
FROM PURCHASE_ORDER po
JOIN FOOD_ITEM fi ON po.fi_id = fi.fi_id
JOIN SCHOOL_PURCHASE_ORDER spo ON po.pur_id = spo.pur_id
JOIN HUB_SCHOOL hs ON spo.sch_id = hs.sch_id
JOIN HUB h ON hs.hub_id = h.hub_id
WHERE h.hub_id = <your_hub_id>
GROUP BY fi.fi_name;



25. " Expired Food Analysis: Discover food items that frequently expire at hubs."

SELECT fi.fi_name, COUNT(DISTINCT fi.fi_id) AS total_food_items
FROM FOOD_ITEM fi
JOIN PRODUCER_FOOD_ITEM pfi ON fi.fi_id = pfi.fi_id
JOIN HUB_PRODUCER hp ON pfi.pro_id = hp.pro_id
JOIN HUB h ON hp.hub_id = h.hub_id
JOIN HUB_SCHOOL hs ON h.hub_id = hs.hub_id
JOIN SCHOOL_PURCHASE_ORDER spo ON hs.sch_id = spo.sch_id
WHERE h.hub_id = <your_hub_id>
  AND fi.fi_est_expiration < CURRENT_DATE
GROUP BY fi.fi_name;



26. "reducing the quantity of a food item by providing the food items ID and quantity to reduce it by"
(this checks to make sure the ammount doesn't fall below zero)

UPDATE FOOD_ITEM
SET fi_quantity =
  CASE
    WHEN fi_quantity - <amount_to_reduce> >= 0 THEN fi_quantity - <amount_to_reduce>
    ELSE 0
  END
WHERE fi_id IN (
    SELECT pfi.fi_id
    FROM PRODUCER_FOOD_ITEM pfi
    JOIN PRODUCER p ON pfi.pro_id = p.pro_id
    WHERE p.pro_id = <your_producer_id>
);



27. Update the pur_total_price in the PURCHASE_ORDER table

UPDATE PURCHASE_ORDER
SET pur_total_price = pur_quantity * fi_cost_per_quantity
FROM FOOD_ITEM
WHERE PURCHASE_ORDER.fi_id = FOOD_ITEM.fi_id;



"""
