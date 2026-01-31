-- ================================================================
-- UPDATE SIP RECORDS ONLY FOR agent_external_id: ag_v49teQwebZsmeXzzYN2GPN
-- Find existing records that meet/nearly meet conditions
-- ================================================================

BEGIN;

-- Calculate date thresholds as strings
CREATE TEMP TABLE date_thresholds AS
SELECT 
    TO_CHAR(NOW() - INTERVAL '6 months', 'YYYY-MM-DD HH24:MI:SS.MS') as six_months_ago,
    TO_CHAR(NOW() - INTERVAL '2 months', 'YYYY-MM-DD HH24:MI:SS.MS') as two_months_ago,
    TO_CHAR(NOW() - INTERVAL '8 months', 'YYYY-MM-DD HH24:MI:SS.MS') as eight_months_ago,
    TO_CHAR(NOW() - INTERVAL '3 months', 'YYYY-MM-DD HH24:MI:SS.MS') as three_months_ago;

-- ----------------------------------------------------------------
-- STEP 1: Find and Update 20 STAGNANT SIPs
-- ----------------------------------------------------------------
-- Condition: is_active='true', created >6mo ago, no step-up

WITH stagnant_candidates AS (
    SELECT sr.sip_meta_id, sr.user_id
    FROM sip_records sr
    WHERE sr.deleted = 'false'
      AND sr.is_active = 'true'
      -- Already old, or we'll make them old
      AND (sr.created_at IS NULL OR sr.created_at < (SELECT six_months_ago FROM date_thresholds))
      -- No step-up configured (or we can set to 0)
      AND (
          (sr.increment_amount IS NULL OR sr.increment_amount = 0)
          OR 
          (sr.increment_percentage IS NULL OR sr.increment_percentage = 0)
      )
    ORDER BY sr.amount DESC NULLS LAST
    LIMIT 20
)
UPDATE sip_records sr
SET 
    agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN',
    is_active = 'true',
    created_at = COALESCE(
        CASE 
            WHEN sr.created_at < (SELECT six_months_ago FROM date_thresholds) 
            THEN sr.created_at
            ELSE (SELECT eight_months_ago FROM date_thresholds)
        END,
        (SELECT eight_months_ago FROM date_thresholds)
    ),
    increment_amount = 0,
    increment_percentage = 0,
    deleted = 'false'
WHERE sr.sip_meta_id IN (SELECT sip_meta_id FROM stagnant_candidates);

-- Also update the users table for these SIPs
UPDATE users u
SET 
    agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN',
    agent_name = 'DINESHKUMAR MOHAN'
WHERE u.user_id IN (
    SELECT DISTINCT sr.user_id 
    FROM sip_records sr 
    WHERE sr.agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN'
);

-- Verify stagnant SIPs
SELECT COUNT(*) as stagnant_sips_updated 
FROM sip_records sr, date_thresholds dt
WHERE sr.agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN'
  AND sr.is_active = 'true'
  AND sr.deleted = 'false'
  AND (sr.created_at IS NULL OR sr.created_at < dt.six_months_ago)
  AND (sr.increment_amount = 0 OR sr.increment_amount IS NULL)
  AND (sr.increment_percentage = 0 OR sr.increment_percentage IS NULL);

-- ----------------------------------------------------------------
-- STEP 2: Find and Update 20 STOPPED SIPs (different records)
-- ----------------------------------------------------------------
-- Condition: success_count>=3, last_success >2mo ago, is_active='true'

WITH stopped_candidates AS (
    SELECT sr.sip_meta_id, sr.user_id
    FROM sip_records sr, date_thresholds dt
    WHERE sr.deleted = 'false'
      AND sr.is_active = 'true'
      -- Exclude already-updated stagnant SIPs
      AND sr.agent_external_id != 'ag_v49teQwebZsmeXzzYN2GPN'
      -- Has decent success count (or we'll set it)
      AND (sr.success_count >= 3 OR sr.success_count IS NULL)
      -- Last success is old, or we'll make it old
      AND (
          sr.latest_success_order_date IS NULL 
          OR sr.latest_success_order_date < dt.two_months_ago
      )
    ORDER BY sr.success_count DESC NULLS LAST, sr.amount DESC NULLS LAST
    LIMIT 20
)
UPDATE sip_records sr
SET 
    agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN',
    is_active = 'true',
    success_count = CASE 
        WHEN sr.success_count >= 3 THEN sr.success_count
        ELSE 5
    END,
    latest_success_order_date = COALESCE(
        CASE 
            WHEN sr.latest_success_order_date < (SELECT two_months_ago FROM date_thresholds)
            THEN sr.latest_success_order_date
            ELSE (SELECT three_months_ago FROM date_thresholds)
        END,
        (SELECT three_months_ago FROM date_thresholds)
    ),
    deleted = 'false'
WHERE sr.sip_meta_id IN (SELECT sip_meta_id FROM stopped_candidates);

-- Also update users for stopped SIPs
UPDATE users u
SET 
    agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN',
    agent_name = 'DINESHKUMAR MOHAN'
WHERE u.user_id IN (
    SELECT DISTINCT sr.user_id 
    FROM sip_records sr 
    WHERE sr.agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN'
)
AND u.agent_external_id != 'ag_v49teQwebZsmeXzzYN2GPN';

-- Verify stopped SIPs
SELECT COUNT(*) as stopped_sips_updated 
FROM sip_records sr, date_thresholds dt
WHERE sr.agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN'
  AND sr.is_active = 'true'
  AND sr.deleted = 'false'
  AND sr.success_count >= 3
  AND (sr.latest_success_order_date IS NULL OR sr.latest_success_order_date < dt.two_months_ago);

-- ----------------------------------------------------------------
-- FINAL SUMMARY
-- ----------------------------------------------------------------
SELECT 
    'SIP SUMMARY' as check_type,
    (SELECT COUNT(DISTINCT user_id) FROM sip_records WHERE agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN') as unique_users,
    (SELECT COUNT(*) FROM sip_records WHERE agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN') as total_sip_records;

-- ----------------------------------------------------------------
-- VERIFY BOTH CONDITIONS ARE MET
-- ----------------------------------------------------------------
SELECT 
    'CONDITION CHECK' as type,
    
    (SELECT COUNT(*) 
     FROM sip_records sr, date_thresholds dt
     WHERE sr.agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN'
       AND sr.is_active = 'true' 
       AND sr.deleted = 'false'
       AND (sr.created_at IS NULL OR sr.created_at < dt.six_months_ago)
       AND (sr.increment_amount = 0 OR sr.increment_amount IS NULL)
       AND (sr.increment_percentage = 0 OR sr.increment_percentage IS NULL)
    ) as stagnant_sips,
    
    (SELECT COUNT(*) 
     FROM sip_records sr, date_thresholds dt
     WHERE sr.agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN'
       AND sr.is_active = 'true'
       AND sr.deleted = 'false'
       AND sr.success_count >= 3
       AND (sr.latest_success_order_date IS NULL OR sr.latest_success_order_date < dt.two_months_ago)
    ) as stopped_sips;

COMMIT;

-- ================================================================
-- ✅ SCRIPT COMPLETE
-- ================================================================
