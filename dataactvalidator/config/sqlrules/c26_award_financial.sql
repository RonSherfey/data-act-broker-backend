-- Each USSGL account balance or subtotal, when totaled by combination of TAS/DEFC provided in File C,
-- should be a subset of, or equal to, the same combinations in File B.

-- This first cte is selecting the sum of 32 elements in File C based on TAS, DEFC, and Submission ID
WITH award_financial_records AS (
    SELECT SUM(af.ussgl480100_undelivered_or_fyb) AS ussgl480100_undelivered_or_fyb_sum_c,
        SUM(af.ussgl480100_undelivered_or_cpe) AS ussgl480100_undelivered_or_cpe_sum_c,
        SUM(af.ussgl483100_undelivered_or_cpe) AS ussgl483100_undelivered_or_cpe_sum_c,
        SUM(af.ussgl488100_upward_adjustm_cpe) AS ussgl488100_upward_adjustm_cpe_sum_c,
        SUM(af.obligations_undelivered_or_fyb) AS obligations_undelivered_or_fyb_sum_c,
        SUM(af.obligations_undelivered_or_cpe) AS obligations_undelivered_or_cpe_sum_c,
        SUM(af.ussgl490100_delivered_orde_fyb) AS ussgl490100_delivered_orde_fyb_sum_c,
        SUM(af.ussgl490100_delivered_orde_cpe) AS ussgl490100_delivered_orde_cpe_sum_c,
        SUM(af.ussgl493100_delivered_orde_cpe) AS ussgl493100_delivered_orde_cpe_sum_c,
        SUM(af.ussgl498100_upward_adjustm_cpe) AS ussgl498100_upward_adjustm_cpe_sum_c,
        SUM(af.obligations_delivered_orde_fyb) AS obligations_delivered_orde_fyb_sum_c,
        SUM(af.obligations_delivered_orde_cpe) AS obligations_delivered_orde_cpe_sum_c,
        SUM(af.ussgl480200_undelivered_or_fyb) AS ussgl480200_undelivered_or_fyb_sum_c,
        SUM(af.ussgl480200_undelivered_or_cpe) AS ussgl480200_undelivered_or_cpe_sum_c,
        SUM(af.ussgl483200_undelivered_or_cpe) AS ussgl483200_undelivered_or_cpe_sum_c,
        SUM(af.ussgl488200_upward_adjustm_cpe) AS ussgl488200_upward_adjustm_cpe_sum_c,
        SUM(af.gross_outlays_undelivered_fyb) AS gross_outlays_undelivered_fyb_sum_c,
        SUM(af.gross_outlays_undelivered_cpe) AS gross_outlays_undelivered_cpe_sum_c,
        SUM(af.ussgl490200_delivered_orde_cpe) AS ussgl490200_delivered_orde_cpe_sum_c,
        SUM(af.ussgl490800_authority_outl_fyb) AS ussgl490800_authority_outl_fyb_sum_c,
        SUM(af.ussgl490800_authority_outl_cpe) AS ussgl490800_authority_outl_cpe_sum_c,
        SUM(af.ussgl498200_upward_adjustm_cpe) AS ussgl498200_upward_adjustm_cpe_sum_c,
        SUM(af.gross_outlays_delivered_or_fyb) AS gross_outlays_delivered_or_fyb_sum_c,
        SUM(af.gross_outlays_delivered_or_cpe) AS gross_outlays_delivered_or_cpe_sum_c,
        SUM(af.gross_outlay_amount_by_awa_fyb) AS gross_outlay_amount_by_awa_fyb_sum_c,
        SUM(af.gross_outlay_amount_by_awa_cpe) AS gross_outlay_amount_by_awa_cpe_sum_c,
        SUM(af.obligations_incurred_byawa_cpe) AS obligations_incurred_byawa_cpe_sum_c,
        SUM(af.ussgl487100_downward_adjus_cpe) AS ussgl487100_downward_adjus_cpe_sum_c,
        SUM(af.ussgl497100_downward_adjus_cpe) AS ussgl497100_downward_adjus_cpe_sum_c,
        SUM(af.ussgl487200_downward_adjus_cpe) AS ussgl487200_downward_adjus_cpe_sum_c,
        SUM(af.ussgl497200_downward_adjus_cpe) AS ussgl497200_downward_adjus_cpe_sum_c,
        SUM(af.deobligations_recov_by_awa_cpe) AS deobligations_recov_by_awa_cpe_sum_c,
        af.tas,
        UPPER(af.disaster_emergency_fund_code) AS "disaster_emergency_fund_code",
        af.display_tas
    FROM award_financial AS af
    WHERE af.submission_id = {0}
    GROUP BY af.tas,
        UPPER(af.disaster_emergency_fund_code),
        af.display_tas,
        af.submission_id),
-- The second cte selects the sum of the corresponding 32 elements in File B
-- Again, the sum is based on TAS, DEFC, and Submission ID
-- We do a FULL OUTER JOIN of this result, as we don't care if TAS/DEFC combinations from File B aren't in File C
object_class_records AS (
    SELECT SUM(op.ussgl480100_undelivered_or_fyb) AS ussgl480100_undelivered_or_fyb_sum_b,
        SUM(op.ussgl480100_undelivered_or_cpe) AS ussgl480100_undelivered_or_cpe_sum_b,
        SUM(op.ussgl483100_undelivered_or_cpe) AS ussgl483100_undelivered_or_cpe_sum_b,
        SUM(op.ussgl488100_upward_adjustm_cpe) AS ussgl488100_upward_adjustm_cpe_sum_b,
        SUM(op.obligations_undelivered_or_fyb) AS obligations_undelivered_or_fyb_sum_b,
        SUM(op.obligations_undelivered_or_cpe) AS obligations_undelivered_or_cpe_sum_b,
        SUM(op.ussgl490100_delivered_orde_fyb) AS ussgl490100_delivered_orde_fyb_sum_b,
        SUM(op.ussgl490100_delivered_orde_cpe) AS ussgl490100_delivered_orde_cpe_sum_b,
        SUM(op.ussgl493100_delivered_orde_cpe) AS ussgl493100_delivered_orde_cpe_sum_b,
        SUM(op.ussgl498100_upward_adjustm_cpe) AS ussgl498100_upward_adjustm_cpe_sum_b,
        SUM(op.obligations_delivered_orde_fyb) AS obligations_delivered_orde_fyb_sum_b,
        SUM(op.obligations_delivered_orde_cpe) AS obligations_delivered_orde_cpe_sum_b,
        SUM(op.ussgl480200_undelivered_or_fyb) AS ussgl480200_undelivered_or_fyb_sum_b,
        SUM(op.ussgl480200_undelivered_or_cpe) AS ussgl480200_undelivered_or_cpe_sum_b,
        SUM(op.ussgl483200_undelivered_or_cpe) AS ussgl483200_undelivered_or_cpe_sum_b,
        SUM(op.ussgl488200_upward_adjustm_cpe) AS ussgl488200_upward_adjustm_cpe_sum_b,
        SUM(op.gross_outlays_undelivered_fyb) AS gross_outlays_undelivered_fyb_sum_b,
        SUM(op.gross_outlays_undelivered_cpe) AS gross_outlays_undelivered_cpe_sum_b,
        SUM(op.ussgl490200_delivered_orde_cpe) AS ussgl490200_delivered_orde_cpe_sum_b,
        SUM(op.ussgl490800_authority_outl_fyb) AS ussgl490800_authority_outl_fyb_sum_b,
        SUM(op.ussgl490800_authority_outl_cpe) AS ussgl490800_authority_outl_cpe_sum_b,
        SUM(op.ussgl498200_upward_adjustm_cpe) AS ussgl498200_upward_adjustm_cpe_sum_b,
        SUM(op.gross_outlays_delivered_or_fyb) AS gross_outlays_delivered_or_fyb_sum_b,
        SUM(op.gross_outlays_delivered_or_cpe) AS gross_outlays_delivered_or_cpe_sum_b,
        SUM(op.gross_outlay_amount_by_pro_fyb) AS gross_outlay_amount_by_pro_fyb_sum_b,
        SUM(op.gross_outlay_amount_by_pro_cpe) AS gross_outlay_amount_by_pro_cpe_sum_b,
        SUM(op.obligations_incurred_by_pr_cpe) AS obligations_incurred_by_pr_cpe_sum_b,
        SUM(op.ussgl487100_downward_adjus_cpe) AS ussgl487100_downward_adjus_cpe_sum_b,
        SUM(op.ussgl497100_downward_adjus_cpe) AS ussgl497100_downward_adjus_cpe_sum_b,
        SUM(op.ussgl487200_downward_adjus_cpe) AS ussgl487200_downward_adjus_cpe_sum_b,
        SUM(op.ussgl497200_downward_adjus_cpe) AS ussgl497200_downward_adjus_cpe_sum_b,
        SUM(op.deobligations_recov_by_pro_cpe) AS deobligations_recov_by_pro_cpe_sum_b,
        op.tas,
        UPPER(op.disaster_emergency_fund_code) AS "disaster_emergency_fund_code"
    FROM object_class_program_activity AS op
    WHERE op.submission_id = {0}
    GROUP BY op.tas,
        UPPER(op.disaster_emergency_fund_code),
        op.submission_id)
SELECT NULL AS "source_row_number",
    award_financial_records.display_tas AS "source_value_tas",
    award_financial_records.disaster_emergency_fund_code AS "source_value_disaster_emergency_fund_code",
    ussgl480100_undelivered_or_fyb_sum_c AS "source_value_ussgl480100_undelivered_or_fyb_sum_c",
    ussgl480100_undelivered_or_cpe_sum_c AS "source_value_ussgl480100_undelivered_or_cpe_sum_c",
    ussgl483100_undelivered_or_cpe_sum_c AS "source_value_ussgl483100_undelivered_or_cpe_sum_c",
    ussgl488100_upward_adjustm_cpe_sum_c AS "source_value_ussgl488100_upward_adjustm_cpe_sum_c",
    obligations_undelivered_or_fyb_sum_c AS "source_value_obligations_undelivered_or_fyb_sum_c",
    obligations_undelivered_or_cpe_sum_c AS "source_value_obligations_undelivered_or_cpe_sum_c",
    ussgl490100_delivered_orde_fyb_sum_c AS "source_value_ussgl490100_delivered_orde_fyb_sum_c",
    ussgl490100_delivered_orde_cpe_sum_c AS "source_value_ussgl490100_delivered_orde_cpe_sum_c",
    ussgl493100_delivered_orde_cpe_sum_c AS "source_value_ussgl493100_delivered_orde_cpe_sum_c",
    ussgl498100_upward_adjustm_cpe_sum_c AS "source_value_ussgl498100_upward_adjustm_cpe_sum_c",
    obligations_delivered_orde_fyb_sum_c AS "source_value_obligations_delivered_orde_fyb_sum_c",
    obligations_delivered_orde_cpe_sum_c AS "source_value_obligations_delivered_orde_cpe_sum_c",
    ussgl480200_undelivered_or_fyb_sum_c AS "source_value_ussgl480200_undelivered_or_fyb_sum_c",
    ussgl480200_undelivered_or_cpe_sum_c AS "source_value_ussgl480200_undelivered_or_cpe_sum_c",
    ussgl483200_undelivered_or_cpe_sum_c AS "source_value_ussgl483200_undelivered_or_cpe_sum_c",
    ussgl488200_upward_adjustm_cpe_sum_c AS "source_value_ussgl488200_upward_adjustm_cpe_sum_c",
    gross_outlays_undelivered_fyb_sum_c AS "source_value_gross_outlays_undelivered_fyb_sum_c",
    gross_outlays_undelivered_cpe_sum_c AS "source_value_gross_outlays_undelivered_cpe_sum_c",
    ussgl490200_delivered_orde_cpe_sum_c AS "source_value_ussgl490200_delivered_orde_cpe_sum_c",
    ussgl490800_authority_outl_fyb_sum_c AS "source_value_ussgl490800_authority_outl_fyb_sum_c",
    ussgl490800_authority_outl_cpe_sum_c AS "source_value_ussgl490800_authority_outl_cpe_sum_c",
    ussgl498200_upward_adjustm_cpe_sum_c AS "source_value_ussgl498200_upward_adjustm_cpe_sum_c",
    gross_outlays_delivered_or_fyb_sum_c AS "source_value_gross_outlays_delivered_or_fyb_sum_c",
    gross_outlays_delivered_or_cpe_sum_c AS "source_value_gross_outlays_delivered_or_cpe_sum_c",
    gross_outlay_amount_by_awa_fyb_sum_c AS "source_value_gross_outlay_amount_by_awa_fyb_sum_c",
    gross_outlay_amount_by_awa_cpe_sum_c AS "source_value_gross_outlay_amount_by_awa_cpe_sum_c",
    obligations_incurred_byawa_cpe_sum_c AS "source_value_obligations_incurred_byawa_cpe_sum_c",
    ussgl487100_downward_adjus_cpe_sum_c AS "source_value_ussgl487100_downward_adjus_cpe_sum_c",
    ussgl497100_downward_adjus_cpe_sum_c AS "source_value_ussgl497100_downward_adjus_cpe_sum_c",
    ussgl487200_downward_adjus_cpe_sum_c AS "source_value_ussgl487200_downward_adjus_cpe_sum_c",
    ussgl497200_downward_adjus_cpe_sum_c AS "source_value_ussgl497200_downward_adjus_cpe_sum_c",
    deobligations_recov_by_awa_cpe_sum_c AS "source_value_deobligations_recov_by_awa_cpe_sum_c",
    ussgl480100_undelivered_or_fyb_sum_b AS "target_value_ussgl480100_undelivered_or_fyb_sum_b",
    ussgl480100_undelivered_or_cpe_sum_b AS "target_value_ussgl480100_undelivered_or_cpe_sum_b",
    ussgl483100_undelivered_or_cpe_sum_b AS "target_value_ussgl483100_undelivered_or_cpe_sum_b",
    ussgl488100_upward_adjustm_cpe_sum_b AS "target_value_ussgl488100_upward_adjustm_cpe_sum_b",
    obligations_undelivered_or_fyb_sum_b AS "target_value_obligations_undelivered_or_fyb_sum_b",
    obligations_undelivered_or_cpe_sum_b AS "target_value_obligations_undelivered_or_cpe_sum_b",
    ussgl490100_delivered_orde_fyb_sum_b AS "target_value_ussgl490100_delivered_orde_fyb_sum_b",
    ussgl490100_delivered_orde_cpe_sum_b AS "target_value_ussgl490100_delivered_orde_cpe_sum_b",
    ussgl493100_delivered_orde_cpe_sum_b AS "target_value_ussgl493100_delivered_orde_cpe_sum_b",
    ussgl498100_upward_adjustm_cpe_sum_b AS "target_value_ussgl498100_upward_adjustm_cpe_sum_b",
    obligations_delivered_orde_fyb_sum_b AS "target_value_obligations_delivered_orde_fyb_sum_b",
    obligations_delivered_orde_cpe_sum_b AS "target_value_obligations_delivered_orde_cpe_sum_b",
    ussgl480200_undelivered_or_fyb_sum_b AS "target_value_ussgl480200_undelivered_or_fyb_sum_b",
    ussgl480200_undelivered_or_cpe_sum_b AS "target_value_ussgl480200_undelivered_or_cpe_sum_b",
    ussgl483200_undelivered_or_cpe_sum_b AS "target_value_ussgl483200_undelivered_or_cpe_sum_b",
    ussgl488200_upward_adjustm_cpe_sum_b AS "target_value_ussgl488200_upward_adjustm_cpe_sum_b",
    gross_outlays_undelivered_fyb_sum_b AS "target_value_gross_outlays_undelivered_fyb_sum_b",
    gross_outlays_undelivered_cpe_sum_b AS "target_value_gross_outlays_undelivered_cpe_sum_b",
    ussgl490200_delivered_orde_cpe_sum_b AS "target_value_ussgl490200_delivered_orde_cpe_sum_b",
    ussgl490800_authority_outl_fyb_sum_b AS "target_value_ussgl490800_authority_outl_fyb_sum_b",
    ussgl490800_authority_outl_cpe_sum_b AS "target_value_ussgl490800_authority_outl_cpe_sum_b",
    ussgl498200_upward_adjustm_cpe_sum_b AS "target_value_ussgl498200_upward_adjustm_cpe_sum_b",
    gross_outlays_delivered_or_fyb_sum_b AS "target_value_gross_outlays_delivered_or_fyb_sum_b",
    gross_outlays_delivered_or_cpe_sum_b AS "target_value_gross_outlays_delivered_or_cpe_sum_b",
    gross_outlay_amount_by_pro_fyb_sum_b AS "target_value_gross_outlay_amount_by_pro_fyb_sum_b",
    gross_outlay_amount_by_pro_cpe_sum_b AS "target_value_gross_outlay_amount_by_pro_cpe_sum_b",
    obligations_incurred_by_pr_cpe_sum_b AS "target_value_obligations_incurred_by_pr_cpe_sum_b",
    ussgl487100_downward_adjus_cpe_sum_b AS "target_value_ussgl487100_downward_adjus_cpe_sum_b",
    ussgl497100_downward_adjus_cpe_sum_b AS "target_value_ussgl497100_downward_adjus_cpe_sum_b",
    ussgl487200_downward_adjus_cpe_sum_b AS "target_value_ussgl487200_downward_adjus_cpe_sum_b",
    ussgl497200_downward_adjus_cpe_sum_b AS "target_value_ussgl497200_downward_adjus_cpe_sum_b",
    deobligations_recov_by_pro_cpe_sum_b AS "target_value_deobligations_recov_by_pro_cpe_sum_b",
    CASE WHEN ussgl480100_undelivered_or_fyb_sum_c < ussgl480100_undelivered_or_fyb_sum_b
        THEN COALESCE(ussgl480100_undelivered_or_fyb_sum_c - ussgl480100_undelivered_or_fyb_sum_b, 0)
        ELSE 0
        END AS "difference_ussgl480100_undelivered_or_fyb_sum",
    CASE WHEN ussgl480100_undelivered_or_cpe_sum_c < ussgl480100_undelivered_or_cpe_sum_b
        THEN COALESCE(ussgl480100_undelivered_or_cpe_sum_c - ussgl480100_undelivered_or_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_ussgl480100_undelivered_or_cpe_sum",
    CASE WHEN ussgl483100_undelivered_or_cpe_sum_c < ussgl483100_undelivered_or_cpe_sum_b
        THEN COALESCE(ussgl483100_undelivered_or_cpe_sum_c - ussgl483100_undelivered_or_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_ussgl483100_undelivered_or_cpe_sum",
    CASE WHEN ussgl488100_upward_adjustm_cpe_sum_c < ussgl488100_upward_adjustm_cpe_sum_b
        THEN COALESCE(ussgl488100_upward_adjustm_cpe_sum_c - ussgl488100_upward_adjustm_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_ussgl488100_upward_adjustm_cpe_sum",
    CASE WHEN obligations_undelivered_or_fyb_sum_c < obligations_undelivered_or_fyb_sum_b
        THEN COALESCE(obligations_undelivered_or_fyb_sum_c - obligations_undelivered_or_fyb_sum_b, 0)
        ELSE 0
        END AS "difference_obligations_undelivered_or_fyb_sum",
    CASE WHEN obligations_undelivered_or_cpe_sum_c < obligations_undelivered_or_cpe_sum_b
        THEN COALESCE(obligations_undelivered_or_cpe_sum_c - obligations_undelivered_or_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_obligations_undelivered_or_cpe_sum",
    CASE WHEN ussgl490100_delivered_orde_fyb_sum_c < ussgl490100_delivered_orde_fyb_sum_b
        THEN COALESCE(ussgl490100_delivered_orde_fyb_sum_c - ussgl490100_delivered_orde_fyb_sum_b, 0)
        ELSE 0
        END AS "difference_ussgl490100_delivered_orde_fyb_sum",
    CASE WHEN ussgl490100_delivered_orde_cpe_sum_c < ussgl490100_delivered_orde_cpe_sum_b
        THEN COALESCE(ussgl490100_delivered_orde_cpe_sum_c - ussgl490100_delivered_orde_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_ussgl490100_delivered_orde_cpe_sum",
    CASE WHEN ussgl493100_delivered_orde_cpe_sum_c < ussgl493100_delivered_orde_cpe_sum_b
        THEN COALESCE(ussgl493100_delivered_orde_cpe_sum_c - ussgl493100_delivered_orde_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_ussgl493100_delivered_orde_cpe_sum",
    CASE WHEN ussgl498100_upward_adjustm_cpe_sum_c < ussgl498100_upward_adjustm_cpe_sum_b
        THEN COALESCE(ussgl498100_upward_adjustm_cpe_sum_c - ussgl498100_upward_adjustm_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_ussgl498100_upward_adjustm_cpe_sum",
    CASE WHEN obligations_delivered_orde_fyb_sum_c < obligations_delivered_orde_fyb_sum_b
        THEN COALESCE(obligations_delivered_orde_fyb_sum_c - obligations_delivered_orde_fyb_sum_b, 0)
        ELSE 0
        END AS "difference_obligations_delivered_orde_fyb_sum",
    CASE WHEN obligations_delivered_orde_cpe_sum_c < obligations_delivered_orde_cpe_sum_b
        THEN COALESCE(obligations_delivered_orde_cpe_sum_c - obligations_delivered_orde_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_obligations_delivered_orde_cpe_sum",
    CASE WHEN ussgl480200_undelivered_or_fyb_sum_c < ussgl480200_undelivered_or_fyb_sum_b
        THEN COALESCE(ussgl480200_undelivered_or_fyb_sum_c - ussgl480200_undelivered_or_fyb_sum_b, 0)
        ELSE 0
        END AS "difference_ussgl480200_undelivered_or_fyb_sum",
    CASE WHEN ussgl480200_undelivered_or_cpe_sum_c < ussgl480200_undelivered_or_cpe_sum_b
        THEN COALESCE(ussgl480200_undelivered_or_cpe_sum_c - ussgl480200_undelivered_or_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_ussgl480200_undelivered_or_cpe_sum",
    CASE WHEN ussgl483200_undelivered_or_cpe_sum_c < ussgl483200_undelivered_or_cpe_sum_b
        THEN COALESCE(ussgl483200_undelivered_or_cpe_sum_c - ussgl483200_undelivered_or_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_ussgl483200_undelivered_or_cpe_sum",
    CASE WHEN ussgl488200_upward_adjustm_cpe_sum_c < ussgl488200_upward_adjustm_cpe_sum_b
        THEN COALESCE(ussgl488200_upward_adjustm_cpe_sum_c - ussgl488200_upward_adjustm_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_ussgl488200_upward_adjustm_cpe_sum",
    CASE WHEN gross_outlays_undelivered_fyb_sum_c < gross_outlays_undelivered_fyb_sum_b
        THEN COALESCE(gross_outlays_undelivered_fyb_sum_c - gross_outlays_undelivered_fyb_sum_b, 0)
        ELSE 0
        END AS "difference_gross_outlays_undelivered_fyb_sum",
    CASE WHEN gross_outlays_undelivered_cpe_sum_c < gross_outlays_undelivered_cpe_sum_b
        THEN COALESCE(gross_outlays_undelivered_cpe_sum_c - gross_outlays_undelivered_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_gross_outlays_undelivered_cpe_sum",
    CASE WHEN ussgl490200_delivered_orde_cpe_sum_c < ussgl490200_delivered_orde_cpe_sum_b
        THEN COALESCE(ussgl490200_delivered_orde_cpe_sum_c - ussgl490200_delivered_orde_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_ussgl490200_delivered_orde_cpe_sum",
    CASE WHEN ussgl490800_authority_outl_fyb_sum_c < ussgl490800_authority_outl_fyb_sum_b
        THEN COALESCE(ussgl490800_authority_outl_fyb_sum_c - ussgl490800_authority_outl_fyb_sum_b, 0)
        ELSE 0
        END AS "difference_ussgl490800_authority_outl_fyb_sum",
    CASE WHEN ussgl490800_authority_outl_cpe_sum_c < ussgl490800_authority_outl_cpe_sum_b
        THEN COALESCE(ussgl490800_authority_outl_cpe_sum_c - ussgl490800_authority_outl_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_ussgl490800_authority_outl_cpe_sum",
    CASE WHEN ussgl498200_upward_adjustm_cpe_sum_c < ussgl498200_upward_adjustm_cpe_sum_b
        THEN COALESCE(ussgl498200_upward_adjustm_cpe_sum_c - ussgl498200_upward_adjustm_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_ussgl498200_upward_adjustm_cpe_sum",
    CASE WHEN gross_outlays_delivered_or_fyb_sum_c < gross_outlays_delivered_or_fyb_sum_b
        THEN COALESCE(gross_outlays_delivered_or_fyb_sum_c - gross_outlays_delivered_or_fyb_sum_b, 0)
        ELSE 0
        END AS "difference_gross_outlays_delivered_or_fyb_sum",
    CASE WHEN gross_outlays_delivered_or_cpe_sum_c < gross_outlays_delivered_or_cpe_sum_b
        THEN COALESCE(gross_outlays_delivered_or_cpe_sum_c - gross_outlays_delivered_or_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_gross_outlays_delivered_or_cpe_sum",
    CASE WHEN gross_outlay_amount_by_awa_fyb_sum_c < gross_outlay_amount_by_pro_fyb_sum_b
        THEN COALESCE(gross_outlay_amount_by_awa_fyb_sum_c - gross_outlay_amount_by_pro_fyb_sum_b, 0)
        ELSE 0
        END AS "difference_gross_outlay_amount_by_pro_fyb_sum",
    CASE WHEN gross_outlay_amount_by_awa_cpe_sum_c < gross_outlay_amount_by_pro_cpe_sum_b
        THEN COALESCE(gross_outlay_amount_by_awa_cpe_sum_c - gross_outlay_amount_by_pro_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_gross_outlay_amount_by_pro_cpe_sum",
    CASE WHEN obligations_incurred_byawa_cpe_sum_c < obligations_incurred_by_pr_cpe_sum_b
        THEN COALESCE(obligations_incurred_byawa_cpe_sum_c - obligations_incurred_by_pr_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_obligations_incurred_by_pr_cpe_sum",
    CASE WHEN ussgl487100_downward_adjus_cpe_sum_c > ussgl487100_downward_adjus_cpe_sum_b
        THEN COALESCE(ussgl487100_downward_adjus_cpe_sum_c - ussgl487100_downward_adjus_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_ussgl487100_downward_adjus_cpe_sum",
    CASE WHEN ussgl497100_downward_adjus_cpe_sum_c > ussgl497100_downward_adjus_cpe_sum_b
        THEN COALESCE(ussgl497100_downward_adjus_cpe_sum_c - ussgl497100_downward_adjus_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_ussgl497100_downward_adjus_cpe_sum",
    CASE WHEN ussgl487200_downward_adjus_cpe_sum_c > ussgl487200_downward_adjus_cpe_sum_b
        THEN COALESCE(ussgl487200_downward_adjus_cpe_sum_c - ussgl487200_downward_adjus_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_ussgl487200_downward_adjus_cpe_sum",
    CASE WHEN ussgl497200_downward_adjus_cpe_sum_c > ussgl497200_downward_adjus_cpe_sum_b
        THEN COALESCE(ussgl497200_downward_adjus_cpe_sum_c - ussgl497200_downward_adjus_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_ussgl497200_downward_adjus_cpe_sum",
    CASE WHEN deobligations_recov_by_awa_cpe_sum_c > deobligations_recov_by_pro_cpe_sum_b
        THEN COALESCE(deobligations_recov_by_awa_cpe_sum_c - deobligations_recov_by_pro_cpe_sum_b, 0)
        ELSE 0
        END AS "difference_deobligations_recov_by_pro_cpe_sum",
    award_financial_records.display_tas AS "uniqueid_TAS",
    award_financial_records.disaster_emergency_fund_code AS "uniqueid_DisasterEmergencyFundCode"
FROM award_financial_records
FULL OUTER JOIN object_class_records
    -- We join the two ctes based on the same TAS and PAC combination
    ON object_class_records.tas = award_financial_records.tas
    AND object_class_records.disaster_emergency_fund_code = award_financial_records.disaster_emergency_fund_code
-- For the final five values, the numbers in file B are expected to be larger than those in file C. For the rest,
-- they are expected to be larger in absolute value but negative, therefore farther left on the number line and smaller
-- in numeric value
WHERE ussgl480100_undelivered_or_fyb_sum_c < ussgl480100_undelivered_or_fyb_sum_b
    OR ussgl480100_undelivered_or_cpe_sum_c < ussgl480100_undelivered_or_cpe_sum_b
    OR ussgl483100_undelivered_or_cpe_sum_c < ussgl483100_undelivered_or_cpe_sum_b
    OR ussgl488100_upward_adjustm_cpe_sum_c < ussgl488100_upward_adjustm_cpe_sum_b
    OR obligations_undelivered_or_fyb_sum_c < obligations_undelivered_or_fyb_sum_b
    OR obligations_undelivered_or_cpe_sum_c < obligations_undelivered_or_cpe_sum_b
    OR ussgl490100_delivered_orde_fyb_sum_c < ussgl490100_delivered_orde_fyb_sum_b
    OR ussgl490100_delivered_orde_cpe_sum_c < ussgl490100_delivered_orde_cpe_sum_b
    OR ussgl493100_delivered_orde_cpe_sum_c < ussgl493100_delivered_orde_cpe_sum_b
    OR ussgl498100_upward_adjustm_cpe_sum_c < ussgl498100_upward_adjustm_cpe_sum_b
    OR obligations_delivered_orde_fyb_sum_c < obligations_delivered_orde_fyb_sum_b
    OR obligations_delivered_orde_cpe_sum_c < obligations_delivered_orde_cpe_sum_b
    OR ussgl480200_undelivered_or_fyb_sum_c < ussgl480200_undelivered_or_fyb_sum_b
    OR ussgl480200_undelivered_or_cpe_sum_c < ussgl480200_undelivered_or_cpe_sum_b
    OR ussgl483200_undelivered_or_cpe_sum_c < ussgl483200_undelivered_or_cpe_sum_b
    OR ussgl488200_upward_adjustm_cpe_sum_c < ussgl488200_upward_adjustm_cpe_sum_b
    OR gross_outlays_undelivered_fyb_sum_c < gross_outlays_undelivered_fyb_sum_b
    OR gross_outlays_undelivered_cpe_sum_c < gross_outlays_undelivered_cpe_sum_b
    OR ussgl490200_delivered_orde_cpe_sum_c < ussgl490200_delivered_orde_cpe_sum_b
    OR ussgl490800_authority_outl_fyb_sum_c < ussgl490800_authority_outl_fyb_sum_b
    OR ussgl490800_authority_outl_cpe_sum_c < ussgl490800_authority_outl_cpe_sum_b
    OR ussgl498200_upward_adjustm_cpe_sum_c < ussgl498200_upward_adjustm_cpe_sum_b
    OR gross_outlays_delivered_or_fyb_sum_c < gross_outlays_delivered_or_fyb_sum_b
    OR gross_outlays_delivered_or_cpe_sum_c < gross_outlays_delivered_or_cpe_sum_b
    OR gross_outlay_amount_by_awa_fyb_sum_c < gross_outlay_amount_by_pro_fyb_sum_b
    OR gross_outlay_amount_by_awa_cpe_sum_c < gross_outlay_amount_by_pro_cpe_sum_b
    OR obligations_incurred_byawa_cpe_sum_c < obligations_incurred_by_pr_cpe_sum_b
    OR ussgl487100_downward_adjus_cpe_sum_c > ussgl487100_downward_adjus_cpe_sum_b
    OR ussgl497100_downward_adjus_cpe_sum_c > ussgl497100_downward_adjus_cpe_sum_b
    OR ussgl487200_downward_adjus_cpe_sum_c > ussgl487200_downward_adjus_cpe_sum_b
    OR ussgl497200_downward_adjus_cpe_sum_c > ussgl497200_downward_adjus_cpe_sum_b
    OR deobligations_recov_by_awa_cpe_sum_c > deobligations_recov_by_pro_cpe_sum_b;
