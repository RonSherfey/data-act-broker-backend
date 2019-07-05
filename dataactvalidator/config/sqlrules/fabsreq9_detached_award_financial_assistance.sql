-- AwardeeOrRecipientLegalEntityName is required for all submissions except delete records, but was not provided in
-- this row.
SELECT
    row_number,
    awardee_or_recipient_legal,
    correction_delete_indicatr
FROM detached_award_financial_assistance
WHERE submission_id = {0}
    AND UPPER(COALESCE(correction_delete_indicatr, '')) <> 'D'
    AND COALESCE(awardee_or_recipient_legal, '') = '';
