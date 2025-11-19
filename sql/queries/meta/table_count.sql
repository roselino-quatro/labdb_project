SELECT COUNT(*) AS table_count
FROM information_schema.tables
WHERE table_schema = current_schema()
  AND table_type = 'BASE TABLE';
