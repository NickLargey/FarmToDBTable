TRUNCATE TABLE school_purchase_order CASCADE;
TRUNCATE TABLE purchase_order CASCADE;
TRUNCATE TABLE producer_food_item CASCADE;
TRUNCATE TABLE food_item CASCADE;
TRUNCATE TABLE hub_school CASCADE;
TRUNCATE TABLE school CASCADE;
TRUNCATE TABLE hub_producer CASCADE;
TRUNCATE TABLE producer CASCADE;
TRUNCATE TABLE hub CASCADE;
TRUNCATE TABLE role_slot CASCADE;
TRUNCATE TABLE hub_role CASCADE;
TRUNCATE TABLE volunteer CASCADE;
TRUNCATE TABLE volunteer_role CASCADE;

-- Reset sequence for the 'school' table
DO $$ 
DECLARE
    table_name text := 'school';
    sequence_name text;
BEGIN
    sequence_name := table_name || '_sch_id_seq';
    IF EXISTS (SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = sequence_name) THEN
        EXECUTE 'ALTER SEQUENCE ' || sequence_name || ' RESTART WITH 1';
    END IF;
END $$;

-- Reset sequence for the 'hub_school' table
DO $$ 
DECLARE
    table_name text := 'hub_school';
    sequence_name text;
BEGIN
    sequence_name := table_name || '_hub_sch_id_seq';
    IF EXISTS (SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = sequence_name) THEN
        EXECUTE 'ALTER SEQUENCE ' || sequence_name || ' RESTART WITH 1';
    END IF;
END $$;

-- Reset sequence for the 'producer' table
DO $$ 
DECLARE
    table_name text := 'producer';
    sequence_name text;
BEGIN
    sequence_name := table_name || '_pro_id_seq';
    IF EXISTS (SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = sequence_name) THEN
        EXECUTE 'ALTER SEQUENCE ' || sequence_name || ' RESTART WITH 1';
    END IF;
END $$;

-- Reset sequence for the 'hub_producer' table
DO $$ 
DECLARE
    table_name text := 'hub_producer';
    sequence_name text;
BEGIN
    sequence_name := table_name || '_hub_pro_id_seq';
    IF EXISTS (SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = sequence_name) THEN
        EXECUTE 'ALTER SEQUENCE ' || sequence_name || ' RESTART WITH 1';
    END IF;
END $$;

-- Reset sequence for the 'food_item' table
DO $$ 
DECLARE
    table_name text := 'food_item';
    sequence_name text;
BEGIN
    sequence_name := table_name || '_fi_id_seq';
    IF EXISTS (SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = sequence_name) THEN
        EXECUTE 'ALTER SEQUENCE ' || sequence_name || ' RESTART WITH 1';
    END IF;
END $$;

-- Reset sequence for the 'producer_food_item' table
DO $$ 
DECLARE
    table_name text := 'producer_food_item';
    sequence_name text;
BEGIN
    sequence_name := table_name || '_pro_fi_id_seq';
    IF EXISTS (SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = sequence_name) THEN
        EXECUTE 'ALTER SEQUENCE ' || sequence_name || ' RESTART WITH 1';
    END IF;
END $$;

-- Reset sequence for the 'purchase_order' table
DO $$ 
DECLARE
    table_name text := 'purchase_order';
    sequence_name text;
BEGIN
    sequence_name := table_name || '_pur_id_seq';
    IF EXISTS (SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = sequence_name) THEN
        EXECUTE 'ALTER SEQUENCE ' || sequence_name || ' RESTART WITH 1';
    END IF;
END $$;

-- Reset sequence for the 'school_purchase_order' table
DO $$ 
DECLARE
    table_name text := 'school_purchase_order';
    sequence_name text;
BEGIN
    sequence_name := table_name || '_sch_pur_id_seq';
    IF EXISTS (SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = sequence_name) THEN
        EXECUTE 'ALTER SEQUENCE ' || sequence_name || ' RESTART WITH 1';
    END IF;
END $$;

-- Reset sequence for the 'volunteer' table
DO $$ 
DECLARE
    table_name text := 'volunteer';
    sequence_name text;
BEGIN
    sequence_name := table_name || '_vol_id_seq';
    IF EXISTS (SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = sequence_name) THEN
        EXECUTE 'ALTER SEQUENCE ' || sequence_name || ' RESTART WITH 1';
    END IF;
END $$;

-- Reset sequence for the 'volunteer_role' table
DO $$ 
DECLARE
    table_name text := 'volunteer_role';
    sequence_name text;
BEGIN
    sequence_name := table_name || '_vol_role_id_seq';
    IF EXISTS (SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = sequence_name) THEN
        EXECUTE 'ALTER SEQUENCE ' || sequence_name || ' RESTART WITH 1';
    END IF;
END $$;

-- Reset sequence for the 'role_slot' table
DO $$ 
DECLARE
    table_name text := 'role_slot';
    sequence_name text;
BEGIN
    sequence_name := table_name || '_rs_id_seq';
    IF EXISTS (SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = sequence_name) THEN
        EXECUTE 'ALTER SEQUENCE ' || sequence_name || ' RESTART WITH 1';
    END IF;
END $$;

-- Reset sequence for the 'hub_role' table
DO $$ 
DECLARE
    table_name text := 'hub_role';
    sequence_name text;
BEGIN
    sequence_name := table_name || '_hub_role_id_seq';
    IF EXISTS (SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = sequence_name) THEN
        EXECUTE 'ALTER SEQUENCE ' || sequence_name || ' RESTART WITH 1';
    END IF;
END $$;

-- Reset sequence for the 'hub' table
DO $$ 
DECLARE
    table_name text := 'hub';
    sequence_name text;
BEGIN
    sequence_name := table_name || '_hub_id_seq';
    IF EXISTS (SELECT 1 FROM pg_sequences WHERE schemaname = 'public' AND sequencename = sequence_name) THEN
        EXECUTE 'ALTER SEQUENCE ' || sequence_name || ' RESTART WITH 1'; 
    END IF;
END $$;
