-- FaceValueOfDirectLoanOrLoanGuarantee is required for loans (i.e., when AssistanceType = 07 or 08).
SELECT
    row_number,
    assistance_type,
    face_value_loan_guarantee,
    afa_generated_unique AS "uniqueid_AssistanceTransactionUniqueKey"
FROM detached_award_financial_assistance
WHERE submission_id = {0}
    AND (assistance_type = '07'
        OR assistance_type = '08'
    )
    AND face_value_loan_guarantee IS NULL
    AND UPPER(COALESCE(correction_delete_indicatr, '')) <> 'D';
