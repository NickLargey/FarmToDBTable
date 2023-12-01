SELECT table_schema || '.' || table_name AS table_full_name,
       (xpath('/row/c/text()', query_to_xml(format('select count(*) as c from %I.%I', table_schema, table_name), false, true, '')))[1]::text::int AS row_count
FROM information_schema.tables
WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
AND table_type = 'BASE TABLE'
ORDER BY table_schema, table_name;
