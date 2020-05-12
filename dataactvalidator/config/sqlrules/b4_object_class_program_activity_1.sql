-- ObligationsDeliveredOrdersUnpaidTotal (FYB) = USSGL 4901 for the same TAS/DEFC combination.
-- This applies to the program activity and object class level.
SELECT
    row_number,
    obligations_delivered_orde_fyb,
    ussgl490100_delivered_orde_fyb,
    COALESCE(obligations_delivered_orde_fyb, 0) - COALESCE(ussgl490100_delivered_orde_fyb, 0) AS "difference",
    display_tas AS "uniqueid_TAS",
    disaster_emergency_fund_code AS "uniqueid_DisasterEmergencyFundCode",
    program_activity_code AS "uniqueid_ProgramActivityCode",
    object_class AS "uniqueid_ObjectClass"
FROM object_class_program_activity
WHERE submission_id = {0}
    AND COALESCE(obligations_delivered_orde_fyb, 0) <> COALESCE(ussgl490100_delivered_orde_fyb, 0);
