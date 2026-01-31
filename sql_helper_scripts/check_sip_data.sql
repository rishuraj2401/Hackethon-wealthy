-- ================================================================
-- INSPECT SIP RECORDS DATA
-- ================================================================

-- Check total count and sample data
SELECT 
    'Total SIP Records' as info,
    COUNT(*) as count
FROM sip_records;

-- Check date column types and sample values
SELECT 
    'Date Column Samples' as info,
    created_at,
    latest_success_order_date,
    pg_typeof(created_at) as created_at_type,
    pg_typeof(latest_success_order_date) as latest_type
FROM sip_records
WHERE created_at IS NOT NULL
LIMIT 5;

-- Check distribution of key fields
SELECT 
    'Field Distribution' as info,
    COUNT(*) as total_records,
    COUNT(CASE WHEN is_active = 'true' THEN 1 END) as active_count,
    COUNT(CASE WHEN deleted = 'false' THEN 1 END) as not_deleted_count,
    COUNT(CASE WHEN increment_amount = 0 OR increment_amount IS NULL THEN 1 END) as no_increment_amount,
    COUNT(CASE WHEN increment_percentage = 0 OR increment_percentage IS NULL THEN 1 END) as no_increment_pct,
    COUNT(CASE WHEN success_count >= 3 THEN 1 END) as success_3plus
FROM sip_records;

-- Find records that could be stagnant (relaxed criteria)
SELECT 
    'Potential Stagnant SIPs' as category,
    COUNT(*) as count
FROM sip_records
WHERE deleted = 'false'
  AND is_active = 'true'
  AND (increment_amount IS NULL OR increment_amount = 0)
  AND (increment_percentage IS NULL OR increment_percentage = 0);

-- Find records that could be stopped (relaxed criteria)
SELECT 
    'Potential Stopped SIPs' as category,
    COUNT(*) as count
FROM sip_records
WHERE deleted = 'false'
  AND is_active = 'true'
  AND success_count >= 3;

-- Sample of active SIPs
SELECT 
    sip_meta_id,
    user_id,
    amount,
    is_active,
    created_at,
    success_count,
    latest_success_order_date,
    increment_amount,
    increment_percentage
FROM sip_records
WHERE deleted = 'false'
  AND is_active = 'true'
ORDER BY amount DESC
LIMIT 10;
