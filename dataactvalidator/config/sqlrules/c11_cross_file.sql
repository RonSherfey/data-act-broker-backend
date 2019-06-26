-- Each unique PIID (or combination of PIID/ParentAwardId) from file C (award financial) should exist in
-- file D1 (award procurement). Do not process if allocation transfer agency is not null and does
-- not match agency ID (per C24, a non-SQL rule negation)
WITH award_financial_c11_{0} AS
    (SELECT transaction_obligated_amou,
        piid,
        parent_award_id,
        row_number,
        allocation_transfer_agency,
        agency_identifier
    FROM award_financial
    WHERE submission_id = {0}),
award_procurement_c11_{0} AS
    (SELECT piid,
        parent_award_id
    FROM award_procurement
    WHERE submission_id = {0}),
-- perform a union so we can have both of these conditions checked without using an OR
unioned_financial_procurement_c11_{0} AS
    (SELECT piid,
        parent_award_id
    FROM award_financial_c11_{0} AS af1
    WHERE af1.parent_award_id IS NULL
        AND NOT EXISTS (
            SELECT 1
            FROM award_procurement_c11_{0} AS ap
            WHERE UPPER(ap.piid) = UPPER(af1.piid)
        )
    UNION
    SELECT piid,
        parent_award_id
    FROM award_financial_c11_{0} AS af2
    WHERE af2.parent_award_id IS NOT NULL
        AND NOT EXISTS (
            SELECT 1
            FROM award_procurement_c11_{0} AS ap
            WHERE UPPER(ap.piid) = UPPER(af2.piid)
                AND COALESCE(ap.parent_award_id, '') = COALESCE(af2.parent_award_id, '')
        ))
SELECT
    af.row_number,
    af.piid,
    af.parent_award_id
FROM award_financial_c11_{0} AS af
WHERE af.transaction_obligated_amou IS NOT NULL
    AND af.piid IS NOT NULL
    AND (COALESCE(af.allocation_transfer_agency, '') = ''
        OR (COALESCE(af.allocation_transfer_agency, '') <> ''
            AND af.allocation_transfer_agency = af.agency_identifier
        )
    )
    -- check the results of the union. We can do this coalesce because the piid and parent_award_id returned are both
    -- from award_financial to begin with so it's won't break anything to join on them
    AND EXISTS (
        SELECT 1
        FROM unioned_financial_procurement_c11_{0} AS ufc
        WHERE UPPER(af.piid) = UPPER(ufc.piid)
            AND COALESCE(af.parent_award_id, '') = COALESCE(ufc.parent_award_id, '')
    );
