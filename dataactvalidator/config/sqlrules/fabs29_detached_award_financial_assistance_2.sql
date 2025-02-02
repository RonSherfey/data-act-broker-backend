-- OriginalLoanSubsidyCost must be blank for non-loans (i.e., when AssistanceType is not 07 or 08).
SELECT
    row_number,
    assistance_type,
    original_loan_subsidy_cost,
    afa_generated_unique AS "uniqueid_AssistanceTransactionUniqueKey"
FROM detached_award_financial_assistance
WHERE submission_id = {0}
    AND assistance_type <> '07'
    AND assistance_type <> '08'
    AND original_loan_subsidy_cost IS NOT NULL
    AND original_loan_subsidy_cost <> 0
    AND UPPER(COALESCE(correction_delete_indicatr, '')) <> 'D';
