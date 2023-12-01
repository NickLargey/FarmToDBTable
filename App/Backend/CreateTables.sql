-- 7 entity tables:
-- HUB, PRODUCER, SCHOOL, FOOD_ITEM, VOLUNTEER, ROLE, PURCHASE_ORDER
--


    CREATE TABLE HUB (
        hub_id SERIAL PRIMARY KEY,
        hub_name TEXT,
        hub_address TEXT,
        hub_city TEXT,
        hub_state VARCHAR(2),
        hub_zip VARCHAR(5),
        hub_hours TEXT,
        hub_county TEXT
	);

        CREATE TABLE PRODUCER (
        pro_id SERIAL PRIMARY KEY,
        pro_name TEXT,
        pro_email TEXT,
        pro_phone TEXT,
        pro_address TEXT,
        pro_city TEXT,
        pro_state VARCHAR(2),
        pro_zip VARCHAR(5),
        pro_county TEXT
);

    CREATE TABLE SCHOOL (
        sch_id SERIAL PRIMARY KEY,
        sch_name TEXT,
        sch_email TEXT,
        sch_phone TEXT,
        sch_address TEXT,
        sch_city TEXT,
        sch_state VARCHAR(2),
        sch_zip VARCHAR(5),
        sch_county TEXT
);

    CREATE TABLE FOOD_ITEM (
        fi_id SERIAL PRIMARY KEY,
        fi_name TEXT,
        fi_description TEXT,
        fi_macro TEXT,
        fi_quantity INT,
        fi_cost_per_quantity DECIMAL(10,2),
        fi_date_harvested DATE,
        fi_est_expiration DATE,
        fi_unit TEXT
);

    CREATE TABLE VOLUNTEER (
        vol_id SERIAL PRIMARY KEY,
        vol_name TEXT,
        vol_email TEXT,
        vol_phone TEXT,
        vol_hub INT REFERENCES HUB(hub_id)
);

    CREATE TABLE ROLE_SLOT (
        vrol_id SERIAL PRIMARY KEY,
        vrol_name TEXT,
        vrol_description TEXT,
        vrol_dates DATE,
        vrol_start_time TIME,
        vrol_end_time TIME
);

-- Enum for Purchase Order Status
CREATE TYPE order_status_enum AS ENUM ('Awaiting Fulfillment', 'Ready at Hub', 'Completed Pickup');

    CREATE TABLE PURCHASE_ORDER (
        pur_id SERIAL PRIMARY KEY,
        pur_date DATE,
        pur_quantity INT,
        pur_total_price DECIMAL(10,2),
        pur_fi_id INT REFERENCES FOOD_ITEM(fi_id),
        pur_status order_status_enum
);



--
-- 6 relationship tables:
-- SCHOOL_PURCHASE_ORDER, HUB_PRODUCER, HUB_SCHOOL,
-- HUB_ROLE, PRODUCER_FOOD_ITEM, VOLUNTEER_ROLE
--

    CREATE TABLE SCHOOL_PURCHASE_ORDER (
        sch_id INT REFERENCES SCHOOL(sch_id),
        pur_id INT REFERENCES PURCHASE_ORDER(pur_id),
        PRIMARY KEY (sch_id, pur_id)
);

    CREATE TABLE HUB_PRODUCER (
        hub_id INT REFERENCES HUB(hub_id),
        pro_id INT REFERENCES PRODUCER(pro_id),
        PRIMARY KEY (hub_id, pro_id)
);

    CREATE TABLE HUB_SCHOOL (
        hub_ID INT REFERENCES HUB(hub_id),
        sch_id INT REFERENCES SCHOOL(sch_id),
        PRIMARY KEY (hub_id, sch_id)
);

	CREATE TABLE HUB_ROLE (
    	hub_id INT REFERENCES HUB(hub_id),
    	vrol_id INT REFERENCES ROLE_SLOT(vrol_id),
    	PRIMARY KEY (hub_id, vrol_id)
);


    CREATE TABLE PRODUCER_FOOD_ITEM (
        pro_id INT REFERENCES PRODUCER(pro_id),
        fi_id INT REFERENCES FOOD_ITEM(fi_id),
        PRIMARY KEY (pro_id, fi_id)
);

    CREATE TABLE VOLUNTEER_ROLE (
        vol_id INT REFERENCES VOLUNTEER(vol_id),
        vrol_id INT REFERENCES ROLE_SLOT(vrol_id),
        PRIMARY KEY (vol_id, vrol_id)
);