-- ================================================================
-- MODIFY 20 ROWS PER TABLE FOR agent_id: 122234
-- agent_external_id: ag_v49teQwebZsmeXzzYN2GPN
-- (Fixed for string date columns)
-- ================================================================

BEGIN;

-- ----------------------------------------------------------------
-- STEP 1: Select and update 20 USERS (with SIP, Insurance, Portfolio data)
-- ----------------------------------------------------------------
WITH target_users AS (
    SELECT DISTINCT u.user_id, u.mf_current_value
    FROM users u
    -- Must have SIP records
    INNER JOIN sip_records sr ON u.user_id = sr.user_id
    -- Must have insurance records
    INNER JOIN insurance_records ir ON u.user_id = ir.user_id
    -- Must have portfolio holdings
    INNER JOIN portfolio_holdings ph ON u.user_id = ph.user_id
    WHERE u.mf_current_value > 500000
      AND u.date_of_birth IS NOT NULL
      AND EXTRACT(YEAR FROM AGE(u.date_of_birth)) >= 30
      AND sr.deleted = 'false'
      AND ir.deleted = 'false'
      AND ph.current_value > 0
    ORDER BY u.mf_current_value DESC
    LIMIT 20
)
UPDATE users
SET 
    agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN',
    agent_name = 'DINESHKUMAR MOHAN'
WHERE user_id IN (SELECT user_id FROM target_users);

CREATE TEMP TABLE temp_target_users AS
SELECT user_id FROM users 
WHERE agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN'
LIMIT 20;

SELECT COUNT(*) as users_updated FROM temp_target_users;

-- ----------------------------------------------------------------
-- STEP 2: Update SIP_RECORDS for STAGNANT SIPs (10 rows)
-- ----------------------------------------------------------------
WITH date_threshold AS (
    SELECT TO_CHAR(NOW() - INTERVAL '6 months', 'YYYY-MM-DD HH24:MI:SS.MS') as six_months_ago,
           TO_CHAR(NOW() - INTERVAL '8 months', 'YYYY-MM-DD HH24:MI:SS.MS') as eight_months_ago
),
sip_targets AS (
    SELECT sr.sip_meta_id
    FROM sip_records sr
    WHERE sr.user_id IN (SELECT user_id FROM temp_target_users)
      AND sr.deleted = 'false'
    ORDER BY sr.amount DESC NULLS LAST
    LIMIT 10
)
UPDATE sip_records
SET 
    agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN',
    is_active = 'true',
    created_at = (SELECT eight_months_ago FROM date_threshold),
    increment_amount = 0,
    increment_percentage = 0,
    deleted = 'false'
WHERE sip_meta_id IN (SELECT sip_meta_id FROM sip_targets);

-- Verify stagnant SIPs
WITH date_threshold AS (
    SELECT TO_CHAR(NOW() - INTERVAL '6 months', 'YYYY-MM-DD HH24:MI:SS.MS') as six_months_ago
)
SELECT COUNT(*) as stagnant_sips_updated 
FROM sip_records, date_threshold
WHERE agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN'
  AND is_active = 'true'
  AND deleted = 'false'
  AND (created_at IS NULL OR created_at < date_threshold.six_months_ago)
  AND (increment_amount = 0 OR increment_amount IS NULL);

-- ----------------------------------------------------------------
-- STEP 3: Update SIP_RECORDS for STOPPED SIPs (10 more rows)
-- ----------------------------------------------------------------
WITH date_threshold AS (
    SELECT TO_CHAR(NOW() - INTERVAL '6 months', 'YYYY-MM-DD HH24:MI:SS.MS') as six_months_ago,
           TO_CHAR(NOW() - INTERVAL '3 months', 'YYYY-MM-DD HH24:MI:SS.MS') as three_months_ago
),
stopped_sip_targets AS (
    SELECT sr.sip_meta_id
    FROM sip_records sr, date_threshold dt
    WHERE sr.user_id IN (SELECT user_id FROM temp_target_users)
      AND sr.deleted = 'false'
      AND sr.sip_meta_id NOT IN (
          SELECT sip_meta_id FROM sip_records, date_threshold
          WHERE agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN'
            AND (created_at IS NULL OR created_at < date_threshold.six_months_ago)
      )
    ORDER BY sr.amount DESC NULLS LAST
    LIMIT 10
)
UPDATE sip_records
SET 
    agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN',
    is_active = 'true',
    success_count = 5,
    latest_success_order_date = (SELECT three_months_ago FROM date_threshold),
    deleted = 'false'
WHERE sip_meta_id IN (SELECT sip_meta_id FROM stopped_sip_targets);

-- Verify stopped SIPs
WITH date_threshold AS (
    SELECT TO_CHAR(NOW() - INTERVAL '2 months', 'YYYY-MM-DD HH24:MI:SS.MS') as two_months_ago
)
SELECT COUNT(*) as stopped_sips_updated 
FROM sip_records, date_threshold
WHERE agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN'
  AND is_active = 'true'
  AND deleted = 'false'
  AND success_count >= 3
  AND (latest_success_order_date IS NULL OR latest_success_order_date < date_threshold.two_months_ago);

-- ----------------------------------------------------------------
-- STEP 4: Update INSURANCE_RECORDS for GAPS (20 rows)
-- ----------------------------------------------------------------
WITH insurance_targets AS (
    SELECT ir.source_id
    FROM insurance_records ir
    WHERE ir.user_id IN (SELECT user_id FROM temp_target_users)
      AND ir.deleted = 'false'
      AND ir.premium > 0
    ORDER BY ir.premium ASC
    LIMIT 20
)
UPDATE insurance_records
SET 
    premium = 100,
    deleted = 'false'
WHERE source_id IN (SELECT source_id FROM insurance_targets);

-- Verify insurance gaps
SELECT COUNT(DISTINCT u.user_id) as insurance_gaps_count
FROM users u
LEFT JOIN (
    SELECT user_id, SUM(premium) as total_premium
    FROM insurance_records
    WHERE deleted = 'false' AND premium > 0
    GROUP BY user_id
) i ON u.user_id = i.user_id
WHERE u.agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN'
  AND u.mf_current_value > 500000
  AND u.date_of_birth IS NOT NULL
  AND (
      (COALESCE(i.total_premium, 0) = 0 AND EXTRACT(YEAR FROM AGE(u.date_of_birth)) >= 30)
      OR COALESCE(i.total_premium, 0) < (u.mf_current_value * 0.001)
  );

-- ----------------------------------------------------------------
-- STEP 5: Update PORTFOLIO_HOLDINGS for REVIEW (20 rows)
-- ----------------------------------------------------------------
WITH portfolio_targets AS (
    SELECT ph.id
    FROM portfolio_holdings ph
    WHERE ph.user_id IN (SELECT user_id FROM temp_target_users)
      AND ph.current_value > 0
      AND ph.live_xirr IS NOT NULL
      AND ph.benchmark_xirr IS NOT NULL
    ORDER BY ph.current_value DESC
    LIMIT 20
)
UPDATE portfolio_holdings
SET 
    live_xirr = CASE 
        WHEN live_xirr < benchmark_xirr THEN live_xirr
        ELSE benchmark_xirr - 2
    END,
    benchmark_xirr = CASE 
        WHEN live_xirr >= benchmark_xirr THEN live_xirr + 3
        ELSE benchmark_xirr
    END
WHERE id IN (SELECT id FROM portfolio_targets);

-- Verify portfolio reviews
SELECT COUNT(*) as portfolio_review_count
FROM portfolio_holdings ph
JOIN users u ON ph.user_id = u.user_id
WHERE u.agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN'
  AND ph.live_xirr < ph.benchmark_xirr
  AND ph.current_value > 0;

-- ----------------------------------------------------------------
-- FINAL SUMMARY
-- ----------------------------------------------------------------
SELECT 
    'SUMMARY' as check_type,
    (SELECT COUNT(*) FROM users WHERE agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN') as users_count,
    (SELECT COUNT(*) FROM sip_records WHERE agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN') as sip_records_count,
    (SELECT COUNT(*) FROM insurance_records ir 
     JOIN users u ON ir.user_id = u.user_id 
     WHERE u.agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN') as insurance_records_count,
    (SELECT COUNT(*) FROM portfolio_holdings ph 
     JOIN users u ON ph.user_id = u.user_id 
     WHERE u.agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN') as portfolio_holdings_count;

-- ----------------------------------------------------------------
-- VERIFY ALL 4 API CONDITIONS ARE MET
-- ----------------------------------------------------------------
WITH date_thresholds AS (
    SELECT 
        TO_CHAR(NOW() - INTERVAL '6 months', 'YYYY-MM-DD HH24:MI:SS.MS') as six_months_ago,
        TO_CHAR(NOW() - INTERVAL '2 months', 'YYYY-MM-DD HH24:MI:SS.MS') as two_months_ago
)
SELECT 
    'CONDITION CHECK' as type,
    (SELECT COUNT(*) FROM sip_records, date_thresholds
     WHERE agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN'
       AND is_active = 'true' 
       AND deleted = 'false'
       AND (created_at IS NULL OR created_at < date_thresholds.six_months_ago)
       AND (increment_amount = 0 OR increment_amount IS NULL)
    ) as stagnant_sips,
    
    (SELECT COUNT(*) FROM sip_records, date_thresholds
     WHERE agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN'
       AND is_active = 'true'
       AND deleted = 'false'
       AND success_count >= 3
       AND (latest_success_order_date IS NULL OR latest_success_order_date < date_thresholds.two_months_ago)
    ) as stopped_sips,
    
    (SELECT COUNT(DISTINCT u.user_id)
     FROM users u
     LEFT JOIN (
         SELECT user_id, SUM(premium) as total_premium
         FROM insurance_records
         WHERE deleted = 'false' AND premium > 0
         GROUP BY user_id
     ) i ON u.user_id = i.user_id
     WHERE u.agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN'
       AND u.mf_current_value > 500000
       AND u.date_of_birth IS NOT NULL
       AND (
           (COALESCE(i.total_premium, 0) = 0 AND EXTRACT(YEAR FROM AGE(u.date_of_birth)) >= 30)
           OR COALESCE(i.total_premium, 0) < (u.mf_current_value * 0.001)
       )
    ) as insurance_gaps,
    
    (SELECT COUNT(DISTINCT u.user_id)
     FROM portfolio_holdings ph
     JOIN users u ON ph.user_id = u.user_id
     WHERE u.agent_external_id = 'ag_v49teQwebZsmeXzzYN2GPN'
       AND ph.live_xirr < ph.benchmark_xirr
       AND ph.current_value > 0
    ) as portfolio_reviews;

COMMIT;

-- ================================================================
-- ✅ SCRIPT COMPLETE
-- ================================================================