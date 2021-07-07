WITH unlinked_subs AS
    (
        SELECT id,
            prime_id,
            sub_id,
            award_id,
            parent_award_id,
            awarding_sub_tier_agency_c
        FROM subaward
        WHERE subaward.unique_award_key IS NULL
            AND subaward.subaward_type = 'sub-contract'),
aw_dap AS
    (SELECT DISTINCT ON (
            UPPER(dap.piid),
            UPPER(dap.parent_award_id),
            UPPER(dap.awarding_sub_tier_agency_c)
        )
        dap.unique_award_key AS unique_award_key,
        dap.piid AS piid,
        dap.idv_type AS idv_type,
        dap.parent_award_id AS parent_award_id,
        dap.award_description as award_description,
        dap.awarding_sub_tier_agency_c AS awarding_sub_tier_agency_c,
        dap.naics_description AS naics_description,
        dap.awarding_agency_code AS awarding_agency_code,
        dap.awarding_agency_name AS awarding_agency_name,
        dap.funding_agency_code AS funding_agency_code,
        dap.funding_agency_name AS funding_agency_name
    FROM detached_award_procurement AS dap
    WHERE EXISTS (
        SELECT 1
        FROM unlinked_subs
        -- Subcontract Award linking logic, should be consistent with FileF SQL and poppulate subcontract SQL
        WHERE UPPER(TRANSLATE(unlinked_subs.award_id, '-', '')) = UPPER(TRANSLATE(dap.piid, '-', ''))
            AND UPPER(TRANSLATE(unlinked_subs.parent_award_id, '-', '')) IS NOT DISTINCT FROM UPPER(TRANSLATE(dap.parent_award_id, '-', ''))
            AND UPPER(unlinked_subs.awarding_sub_tier_agency_c) = UPPER(dap.awarding_sub_tier_agency_c)
        )
        {0}
    ORDER BY UPPER(dap.piid), UPPER(dap.parent_award_id), UPPER(dap.awarding_sub_tier_agency_c), dap.action_date)
UPDATE subaward
SET
    unique_award_key = aw_dap.unique_award_key,
    awarding_agency_code = aw_dap.awarding_agency_code,
    awarding_agency_name = aw_dap.awarding_agency_name,
    funding_agency_code = aw_dap.funding_agency_code,
    funding_agency_name = aw_dap.funding_agency_name,
    award_description = aw_dap.award_description,
    naics_description = aw_dap.naics_description
FROM unlinked_subs
    JOIN aw_dap
        -- Subcontract Award linking logic, should be consistent with FileF SQL and poppulate subcontract SQL
        ON UPPER(TRANSLATE(unlinked_subs.award_id, '-', '')) = UPPER(TRANSLATE(aw_dap.piid, '-', ''))
        AND UPPER(TRANSLATE(unlinked_subs.parent_award_id, '-', '')) IS NOT DISTINCT FROM UPPER(TRANSLATE(aw_dap.parent_award_id, '-', ''))
        AND UPPER(unlinked_subs.awarding_sub_tier_agency_c) = UPPER(aw_dap.awarding_sub_tier_agency_c)
WHERE subaward.id = unlinked_subs.id;
