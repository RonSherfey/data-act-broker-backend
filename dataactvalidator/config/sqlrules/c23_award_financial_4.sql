-- For each unique URI for financial assistance in File C (award financial), the sum of each TransactionObligatedAmount
-- submitted in the reporting period should match (in inverse) the sum of the FederalActionObligation and
-- OriginalLoanSubsidyCost amounts reported in D2 (award financial assistance) for the same timeframe, regardless of
-- modifications. This rule does not apply if the ATA field is populated and is different from the Agency ID.
WITH award_financial_c23_4_{0} AS
    (SELECT transaction_obligated_amou,
        UPPER(uri) AS uri,
        allocation_transfer_agency,
        agency_identifier
    FROM award_financial
    WHERE submission_id = {0}),
-- gather the grouped sum from the previous WITH (we need both so we can do the NOT EXISTS later)
award_financial_grouped_c23_4_{0} AS
    (SELECT UPPER(uri) AS uri,
        SUM(transaction_obligated_amou) AS sum_ob_amount
    FROM award_financial_c23_4_{0}
    WHERE transaction_obligated_amou IS NOT NULL
    GROUP BY UPPER(uri)),
-- gather the grouped sum for award financial assistance data
award_financial_assistance_c23_4_{0} AS
    (SELECT UPPER(uri) AS uri,
        COALESCE(SUM(CASE WHEN COALESCE(assistance_type, '') IN ('07', '08')
                        THEN original_loan_subsidy_cost::NUMERIC
                        ELSE 0
                    END), 0) AS sum_orig_loan_sub_amount,
        COALESCE(SUM(CASE WHEN COALESCE(assistance_type, '') NOT IN ('07', '08')
                        THEN federal_action_obligation
                        ELSE 0
                    END), 0) AS sum_fed_act_ob_amount
    FROM award_financial_assistance
    WHERE submission_id = {0}
        AND record_type = '1'
    GROUP BY UPPER(uri))
SELECT
    NULL AS "source_row_number",
    af.uri AS "source_value_uri",
    af.sum_ob_amount AS "source_value_transaction_obligated_amou_sum",
    afa.sum_fed_act_ob_amount AS "target_value_federal_action_obligation_sum",
    afa.sum_orig_loan_sub_amount AS "target_value_original_loan_subsidy_cost_sum",
    af.sum_ob_amount - (-1 * afa.sum_fed_act_ob_amount - afa.sum_orig_loan_sub_amount) AS "difference",
    af.uri AS "uniqueid_URI"
FROM award_financial_grouped_c23_4_{0} AS af
JOIN award_financial_assistance_c23_4_{0} AS afa
    ON af.uri = afa.uri
WHERE af.sum_ob_amount <> -1 * afa.sum_fed_act_ob_amount - afa.sum_orig_loan_sub_amount
    AND NOT EXISTS (
        SELECT 1
        FROM award_financial_c23_4_{0} AS sub_af
        WHERE sub_af.uri = af.uri
            AND COALESCE(sub_af.allocation_transfer_agency, '') <> ''
            AND sub_af.allocation_transfer_agency <> sub_af.agency_identifier
    );
