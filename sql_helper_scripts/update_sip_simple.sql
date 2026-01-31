-- ================================================================
-- SIMPLE SIP UPDATE FOR agent_external_id: ag_v49teQwebZsmeXzzYN2GPN
-- Works with existing data, no complex date parsing
-- ================================================================

BEGIN;

-- ----------------------------------------------------------------
-- STEP 1: Update 20 STAGNANT SIPs
-- ----------------------------------------------------------------
-- Criteria: is_active='true', no step-up (increment=0)
-- We'll pick records from 2023 which are already >6 months old

WITH stagnant_targets AS (
    SELECT sip_meta_id, user_id
    FROM sip_records
    WHERE deleted = 'false'
      AND is_active = 'true'
      AND (increment_amount IS NULL OR increment_amount = 0)
      AND (increment_percentage IS NULL OR increment_percentage = 0)
      AND created_at LIKE '%2023%'  -- Old records from 2023
    ORDER BY amount DESC
    LIMIT 20
)
UPDATE sip_records
SET agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN'
WHERE sip_meta_id IN (SELECT sip_meta_id FROM stagnant_targets);

SELECT COUNT(*) as stagnant_sips_updated 
FROM sip_records
WHERE agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN';

-- ----------------------------------------------------------------
-- STEP 2: Update 20 STOPPED SIPs (different from stagnant)
-- ----------------------------------------------------------------
-- Criteria: success_count>=3, last success in 2022 or early 2024 (>2 months ago)

WITH stopped_targets AS (
    SELECT sip_meta_id, user_id
    FROM sip_records
    WHERE deleted = 'false'
      AND is_active = 'true'
      AND success_count >= 3
      -- Old last success date (2022 or before Nov 2025 = >2 months ago)
      AND (
          latest_success_order_date LIKE '%2022%' 
          OR latest_success_order_date LIKE '%2023%'
          OR latest_success_order_date LIKE '%2024%'
      )
      -- Exclude already updated stagnant SIPs
      AND (agent_external_id IS NULL OR agent_external_id != 'ag_v49teQwebZsmeXzzYN2GPN')
    ORDER BY success_count DESC, amount DESC
    LIMIT 20
)
UPDATE sip_records
SET agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN'
WHERE sip_meta_id IN (SELECT sip_meta_id FROM stopped_targets);

SELECT COUNT(*) as total_sips_after_stopped 
FROM sip_records
WHERE agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN';

-- ----------------------------------------------------------------
-- STEP 3: Update users table for these SIPs
-- ----------------------------------------------------------------
UPDATE users
SET 
    agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN',
    agent_name = 'DINESHKUMAR MOHAN'
WHERE user_id IN (
    SELECT DISTINCT user_id 
    FROM sip_records 
    WHERE agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN'
);

SELECT COUNT(DISTINCT user_id) as users_updated
FROM sip_records 
WHERE agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN';

-- ----------------------------------------------------------------
-- FINAL VERIFICATION
-- ----------------------------------------------------------------

-- Count stagnant SIPs (created in 2023, no increment)
SELECT 
    'STAGNANT SIPS' as type,
    COUNT(*) as count
FROM sip_records
WHERE agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN'
  AND is_active = 'true'
  AND deleted = 'false'
  AND created_at LIKE '%2023%'
  AND (increment_amount IS NULL OR increment_amount = 0)
  AND (increment_percentage IS NULL OR increment_percentage = 0);

-- Count stopped SIPs (success_count>=3, old last success)
SELECT 
    'STOPPED SIPS' as type,
    COUNT(*) as count
FROM sip_records
WHERE agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN'
  AND is_active = 'true'
  AND deleted = 'false'
  AND success_count >= 3
  AND (
      latest_success_order_date LIKE '%2022%' 
      OR latest_success_order_date LIKE '%2023%'
      OR latest_success_order_date LIKE '%2024%'
  );

-- Summary
SELECT 
    'SUMMARY' as info,
    COUNT(DISTINCT user_id) as unique_users,
    COUNT(*) as total_sip_records,
    SUM(CASE WHEN created_at LIKE '%2023%' 
             AND (increment_amount = 0 OR increment_amount IS NULL)
             AND (increment_percentage = 0 OR increment_percentage IS NULL)
        THEN 1 ELSE 0 END) as stagnant_count,
    SUM(CASE WHEN success_count >= 3 
             AND (latest_success_order_date LIKE '%2022%' 
                  OR latest_success_order_date LIKE '%2023%'
                  OR latest_success_order_date LIKE '%2024%')
        THEN 1 ELSE 0 END) as stopped_count
FROM sip_records
WHERE agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN'
  AND is_active = 'true'
  AND deleted = 'false';

COMMIT;

-- ================================================================
-- ✅ DONE! Now test the APIs with agent_external_id=ag_v49teQwebZsmeXzzYN2GPN
-- ================================================================
