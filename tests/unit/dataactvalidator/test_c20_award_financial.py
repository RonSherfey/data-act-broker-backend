from random import randint

from tests.unit.dataactcore.factories.staging import AwardFinancialFactory
from tests.unit.dataactcore.factories.staging import ObjectClassProgramActivityFactory
from tests.unit.dataactvalidator.utils import number_of_errors, query_columns


_FILE = 'c20_award_financial'

af_dict = dict(
    submission_id=randint(1000, 10000),
    tas='some-tas',
    object_class='some-class',
    by_direct_reimbursable_fun='some-dr',
    ussgl480100_undelivered_or_fyb=randint(-10000, -1000),
    ussgl480100_undelivered_or_cpe=randint(-10000, -1000),
    ussgl483100_undelivered_or_cpe=randint(-10000, -1000),
    ussgl488100_upward_adjustm_cpe=randint(-10000, -1000),
    obligations_undelivered_or_fyb=randint(-10000, -1000),
    obligations_undelivered_or_cpe=randint(-10000, -1000),
    ussgl490100_delivered_orde_fyb=randint(-10000, -1000),
    ussgl490100_delivered_orde_cpe=randint(-10000, -1000),
    ussgl493100_delivered_orde_cpe=randint(-10000, -1000),
    ussgl498100_upward_adjustm_cpe=randint(-10000, -1000),
    obligations_delivered_orde_fyb=randint(-10000, -1000),
    obligations_delivered_orde_cpe=randint(-10000, -1000),
    ussgl480200_undelivered_or_fyb=randint(-10000, -1000),
    ussgl480200_undelivered_or_cpe=randint(-10000, -1000),
    ussgl483200_undelivered_or_cpe=randint(-10000, -1000),
    ussgl488200_upward_adjustm_cpe=randint(-10000, -1000),
    gross_outlays_undelivered_fyb=randint(-10000, -1000),
    gross_outlays_undelivered_cpe=randint(-10000, -1000),
    ussgl490200_delivered_orde_cpe=randint(-10000, -1000),
    ussgl490800_authority_outl_fyb=randint(-10000, -1000),
    ussgl490800_authority_outl_cpe=randint(-10000, -1000),
    ussgl498200_upward_adjustm_cpe=randint(-10000, -1000),
    gross_outlays_delivered_or_fyb=randint(-10000, -1000),
    gross_outlays_delivered_or_cpe=randint(-10000, -1000),
    gross_outlay_amount_by_awa_fyb=randint(-10000, -1000),
    gross_outlay_amount_by_awa_cpe=randint(-10000, -1000),
    obligations_incurred_byawa_cpe=randint(-10000, -1000),
    ussgl487100_downward_adjus_cpe=randint(-10000, -1000),
    ussgl497100_downward_adjus_cpe=randint(-10000, -1000),
    ussgl487200_downward_adjus_cpe=randint(-10000, -1000),
    ussgl497200_downward_adjus_cpe=randint(-10000, -1000),
    deobligations_recov_by_awa_cpe=randint(-10000, -1000)
)


def test_column_headers(database):
    expected_subset = {
        'source_row_number', 'source_value_tas', 'source_value_object_class',
        'source_value_ussgl480100_undelivered_or_fyb_sum_c', 'source_value_ussgl480100_undelivered_or_cpe_sum_c',
        'source_value_ussgl483100_undelivered_or_cpe_sum_c', 'source_value_ussgl488100_upward_adjustm_cpe_sum_c',
        'source_value_obligations_undelivered_or_fyb_sum_c', 'source_value_obligations_undelivered_or_cpe_sum_c',
        'source_value_ussgl490100_delivered_orde_fyb_sum_c', 'source_value_ussgl490100_delivered_orde_cpe_sum_c',
        'source_value_ussgl493100_delivered_orde_cpe_sum_c', 'source_value_ussgl498100_upward_adjustm_cpe_sum_c',
        'source_value_obligations_delivered_orde_fyb_sum_c', 'source_value_obligations_delivered_orde_cpe_sum_c',
        'source_value_ussgl480200_undelivered_or_fyb_sum_c', 'source_value_ussgl480200_undelivered_or_cpe_sum_c',
        'source_value_ussgl483200_undelivered_or_cpe_sum_c', 'source_value_ussgl488200_upward_adjustm_cpe_sum_c',
        'source_value_gross_outlays_undelivered_fyb_sum_c', 'source_value_gross_outlays_undelivered_cpe_sum_c',
        'source_value_ussgl490200_delivered_orde_cpe_sum_c', 'source_value_ussgl490800_authority_outl_fyb_sum_c',
        'source_value_ussgl490800_authority_outl_cpe_sum_c', 'source_value_ussgl498200_upward_adjustm_cpe_sum_c',
        'source_value_gross_outlays_delivered_or_fyb_sum_c', 'source_value_gross_outlays_delivered_or_cpe_sum_c',
        'source_value_gross_outlay_amount_by_awa_fyb_sum_c', 'source_value_gross_outlay_amount_by_awa_cpe_sum_c',
        'source_value_obligations_incurred_byawa_cpe_sum_c', 'source_value_ussgl487100_downward_adjus_cpe_sum_c',
        'source_value_ussgl497100_downward_adjus_cpe_sum_c', 'source_value_ussgl487200_downward_adjus_cpe_sum_c',
        'source_value_ussgl497200_downward_adjus_cpe_sum_c', 'source_value_deobligations_recov_by_awa_cpe_sum_c',
        'target_value_ussgl480100_undelivered_or_fyb_sum_b', 'target_value_ussgl480100_undelivered_or_cpe_sum_b',
        'target_value_ussgl483100_undelivered_or_cpe_sum_b', 'target_value_ussgl488100_upward_adjustm_cpe_sum_b',
        'target_value_obligations_undelivered_or_fyb_sum_b', 'target_value_obligations_undelivered_or_cpe_sum_b',
        'target_value_ussgl490100_delivered_orde_fyb_sum_b', 'target_value_ussgl490100_delivered_orde_cpe_sum_b',
        'target_value_ussgl493100_delivered_orde_cpe_sum_b', 'target_value_ussgl498100_upward_adjustm_cpe_sum_b',
        'target_value_obligations_delivered_orde_fyb_sum_b', 'target_value_obligations_delivered_orde_cpe_sum_b',
        'target_value_ussgl480200_undelivered_or_fyb_sum_b', 'target_value_ussgl480200_undelivered_or_cpe_sum_b',
        'target_value_ussgl483200_undelivered_or_cpe_sum_b', 'target_value_ussgl488200_upward_adjustm_cpe_sum_b',
        'target_value_gross_outlays_undelivered_fyb_sum_b', 'target_value_gross_outlays_undelivered_cpe_sum_b',
        'target_value_ussgl490200_delivered_orde_cpe_sum_b', 'target_value_ussgl490800_authority_outl_fyb_sum_b',
        'target_value_ussgl490800_authority_outl_cpe_sum_b', 'target_value_ussgl498200_upward_adjustm_cpe_sum_b',
        'target_value_gross_outlays_delivered_or_fyb_sum_b', 'target_value_gross_outlays_delivered_or_cpe_sum_b',
        'target_value_gross_outlay_amount_by_pro_fyb_sum_b', 'target_value_gross_outlay_amount_by_pro_cpe_sum_b',
        'target_value_obligations_incurred_by_pr_cpe_sum_b', 'target_value_ussgl487100_downward_adjus_cpe_sum_b',
        'target_value_ussgl497100_downward_adjus_cpe_sum_b', 'target_value_ussgl487200_downward_adjus_cpe_sum_b',
        'target_value_ussgl497200_downward_adjus_cpe_sum_b', 'target_value_deobligations_recov_by_pro_cpe_sum_b',
        'difference', 'uniqueid_TAS', 'uniqueid_ObjectClass'
    }
    actual = set(query_columns(_FILE, database))
    assert expected_subset == actual


def test_success(database):
    """
        Tests that each USSGL account balance or subtotal, when totaled by combination of TAS, object class code, and
        direct/reimbursable flag provided in File C, should be a subset of, or equal to, the same combinations in File B
    """
    af1 = AwardFinancialFactory(**af_dict)
    af2 = AwardFinancialFactory(**af_dict)

    op1 = ObjectClassProgramActivityFactory(
        ussgl480100_undelivered_or_fyb=af_dict['ussgl480100_undelivered_or_fyb'] - 2,
        ussgl480100_undelivered_or_cpe=af_dict['ussgl480100_undelivered_or_cpe'] - 2,
        ussgl483100_undelivered_or_cpe=af_dict['ussgl483100_undelivered_or_cpe'] - 2,
        ussgl488100_upward_adjustm_cpe=af_dict['ussgl488100_upward_adjustm_cpe'] - 2,
        obligations_undelivered_or_fyb=af_dict['obligations_undelivered_or_fyb'] - 2,
        obligations_undelivered_or_cpe=af_dict['obligations_undelivered_or_cpe'] - 2,
        ussgl490100_delivered_orde_fyb=af_dict['ussgl490100_delivered_orde_fyb'] - 2,
        ussgl490100_delivered_orde_cpe=af_dict['ussgl490100_delivered_orde_cpe'] - 2,
        ussgl493100_delivered_orde_cpe=af_dict['ussgl493100_delivered_orde_cpe'] - 2,
        ussgl498100_upward_adjustm_cpe=af_dict['ussgl498100_upward_adjustm_cpe'] - 2,
        obligations_delivered_orde_fyb=af_dict['obligations_delivered_orde_fyb'] - 2,
        obligations_delivered_orde_cpe=af_dict['obligations_delivered_orde_cpe'] - 2,
        ussgl480200_undelivered_or_fyb=af_dict['ussgl480200_undelivered_or_fyb'] - 2,
        ussgl480200_undelivered_or_cpe=af_dict['ussgl480200_undelivered_or_cpe'] - 2,
        ussgl483200_undelivered_or_cpe=af_dict['ussgl483200_undelivered_or_cpe'] - 2,
        ussgl488200_upward_adjustm_cpe=af_dict['ussgl488200_upward_adjustm_cpe'] - 2,
        gross_outlays_undelivered_fyb=af_dict['gross_outlays_undelivered_fyb'] - 2,
        gross_outlays_undelivered_cpe=af_dict['gross_outlays_undelivered_cpe'] - 2,
        ussgl490200_delivered_orde_cpe=af_dict['ussgl490200_delivered_orde_cpe'] - 2,
        ussgl490800_authority_outl_fyb=af_dict['ussgl490800_authority_outl_fyb'] - 2,
        ussgl490800_authority_outl_cpe=af_dict['ussgl490800_authority_outl_cpe'] - 2,
        ussgl498200_upward_adjustm_cpe=af_dict['ussgl498200_upward_adjustm_cpe'] - 2,
        gross_outlays_delivered_or_fyb=af_dict['gross_outlays_delivered_or_fyb'] - 2,
        gross_outlays_delivered_or_cpe=af_dict['gross_outlays_delivered_or_cpe'] - 2,
        gross_outlay_amount_by_pro_fyb=af_dict['gross_outlay_amount_by_awa_fyb'] - 2,
        gross_outlay_amount_by_pro_cpe=af_dict['gross_outlay_amount_by_awa_cpe'] - 2,
        obligations_incurred_by_pr_cpe=af_dict['obligations_incurred_byawa_cpe'] - 2,
        ussgl487100_downward_adjus_cpe=af_dict['ussgl487100_downward_adjus_cpe'] + 2,
        ussgl497100_downward_adjus_cpe=af_dict['ussgl497100_downward_adjus_cpe'] + 2,
        ussgl487200_downward_adjus_cpe=af_dict['ussgl487200_downward_adjus_cpe'] + 2,
        ussgl497200_downward_adjus_cpe=af_dict['ussgl497200_downward_adjus_cpe'] + 2,
        deobligations_recov_by_pro_cpe=af_dict['deobligations_recov_by_awa_cpe'] + 2,
        tas=af_dict['tas'],
        object_class=af_dict['object_class'],
        by_direct_reimbursable_fun=af_dict['by_direct_reimbursable_fun'],
        submission_id=af_dict['submission_id']
    )

    op2 = ObjectClassProgramActivityFactory(
        ussgl480100_undelivered_or_fyb=af_dict['ussgl480100_undelivered_or_fyb'] - 2,
        ussgl480100_undelivered_or_cpe=af_dict['ussgl480100_undelivered_or_cpe'] - 2,
        ussgl483100_undelivered_or_cpe=af_dict['ussgl483100_undelivered_or_cpe'] - 2,
        ussgl488100_upward_adjustm_cpe=af_dict['ussgl488100_upward_adjustm_cpe'] - 2,
        obligations_undelivered_or_fyb=af_dict['obligations_undelivered_or_fyb'] - 2,
        obligations_undelivered_or_cpe=af_dict['obligations_undelivered_or_cpe'] - 2,
        ussgl490100_delivered_orde_fyb=af_dict['ussgl490100_delivered_orde_fyb'] - 2,
        ussgl490100_delivered_orde_cpe=af_dict['ussgl490100_delivered_orde_cpe'] - 2,
        ussgl493100_delivered_orde_cpe=af_dict['ussgl493100_delivered_orde_cpe'] - 2,
        ussgl498100_upward_adjustm_cpe=af_dict['ussgl498100_upward_adjustm_cpe'] - 2,
        obligations_delivered_orde_fyb=af_dict['obligations_delivered_orde_fyb'] - 2,
        obligations_delivered_orde_cpe=af_dict['obligations_delivered_orde_cpe'] - 2,
        ussgl480200_undelivered_or_fyb=af_dict['ussgl480200_undelivered_or_fyb'] - 2,
        ussgl480200_undelivered_or_cpe=af_dict['ussgl480200_undelivered_or_cpe'] - 2,
        ussgl483200_undelivered_or_cpe=af_dict['ussgl483200_undelivered_or_cpe'] - 2,
        ussgl488200_upward_adjustm_cpe=af_dict['ussgl488200_upward_adjustm_cpe'] - 2,
        gross_outlays_undelivered_fyb=af_dict['gross_outlays_undelivered_fyb'] - 2,
        gross_outlays_undelivered_cpe=af_dict['gross_outlays_undelivered_cpe'] - 2,
        ussgl490200_delivered_orde_cpe=af_dict['ussgl490200_delivered_orde_cpe'] - 2,
        ussgl490800_authority_outl_fyb=af_dict['ussgl490800_authority_outl_fyb'] - 2,
        ussgl490800_authority_outl_cpe=af_dict['ussgl490800_authority_outl_cpe'] - 2,
        ussgl498200_upward_adjustm_cpe=af_dict['ussgl498200_upward_adjustm_cpe'] - 2,
        gross_outlays_delivered_or_fyb=af_dict['gross_outlays_delivered_or_fyb'] - 2,
        gross_outlays_delivered_or_cpe=af_dict['gross_outlays_delivered_or_cpe'] - 2,
        gross_outlay_amount_by_pro_fyb=af_dict['gross_outlay_amount_by_awa_fyb'] - 2,
        gross_outlay_amount_by_pro_cpe=af_dict['gross_outlay_amount_by_awa_cpe'] - 2,
        obligations_incurred_by_pr_cpe=af_dict['obligations_incurred_byawa_cpe'] - 2,
        ussgl487100_downward_adjus_cpe=af_dict['ussgl487100_downward_adjus_cpe'] + 2,
        ussgl497100_downward_adjus_cpe=af_dict['ussgl497100_downward_adjus_cpe'] + 2,
        ussgl487200_downward_adjus_cpe=af_dict['ussgl487200_downward_adjus_cpe'] + 2,
        ussgl497200_downward_adjus_cpe=af_dict['ussgl497200_downward_adjus_cpe'] + 2,
        deobligations_recov_by_pro_cpe=af_dict['deobligations_recov_by_awa_cpe'] + 2,
        tas='some-other-tas',
        object_class=af_dict['object_class'],
        by_direct_reimbursable_fun=af_dict['by_direct_reimbursable_fun'],
        submission_id=af_dict['submission_id']
    )

    op3 = ObjectClassProgramActivityFactory(
        ussgl480100_undelivered_or_fyb=af_dict['ussgl480100_undelivered_or_fyb'] - 2,
        ussgl480100_undelivered_or_cpe=af_dict['ussgl480100_undelivered_or_cpe'] - 2,
        ussgl483100_undelivered_or_cpe=af_dict['ussgl483100_undelivered_or_cpe'] - 2,
        ussgl488100_upward_adjustm_cpe=af_dict['ussgl488100_upward_adjustm_cpe'] - 2,
        obligations_undelivered_or_fyb=af_dict['obligations_undelivered_or_fyb'] - 2,
        obligations_undelivered_or_cpe=af_dict['obligations_undelivered_or_cpe'] - 2,
        ussgl490100_delivered_orde_fyb=af_dict['ussgl490100_delivered_orde_fyb'] - 2,
        ussgl490100_delivered_orde_cpe=af_dict['ussgl490100_delivered_orde_cpe'] - 2,
        ussgl493100_delivered_orde_cpe=af_dict['ussgl493100_delivered_orde_cpe'] - 2,
        ussgl498100_upward_adjustm_cpe=af_dict['ussgl498100_upward_adjustm_cpe'] - 2,
        obligations_delivered_orde_fyb=af_dict['obligations_delivered_orde_fyb'] - 2,
        obligations_delivered_orde_cpe=af_dict['obligations_delivered_orde_cpe'] - 2,
        ussgl480200_undelivered_or_fyb=af_dict['ussgl480200_undelivered_or_fyb'] - 2,
        ussgl480200_undelivered_or_cpe=af_dict['ussgl480200_undelivered_or_cpe'] - 2,
        ussgl483200_undelivered_or_cpe=af_dict['ussgl483200_undelivered_or_cpe'] - 2,
        ussgl488200_upward_adjustm_cpe=af_dict['ussgl488200_upward_adjustm_cpe'] - 2,
        gross_outlays_undelivered_fyb=af_dict['gross_outlays_undelivered_fyb'] - 2,
        gross_outlays_undelivered_cpe=af_dict['gross_outlays_undelivered_cpe'] - 2,
        ussgl490200_delivered_orde_cpe=af_dict['ussgl490200_delivered_orde_cpe'] - 2,
        ussgl490800_authority_outl_fyb=af_dict['ussgl490800_authority_outl_fyb'] - 2,
        ussgl490800_authority_outl_cpe=af_dict['ussgl490800_authority_outl_cpe'] - 2,
        ussgl498200_upward_adjustm_cpe=af_dict['ussgl498200_upward_adjustm_cpe'] - 2,
        gross_outlays_delivered_or_fyb=af_dict['gross_outlays_delivered_or_fyb'] - 2,
        gross_outlays_delivered_or_cpe=af_dict['gross_outlays_delivered_or_cpe'] - 2,
        gross_outlay_amount_by_pro_fyb=af_dict['gross_outlay_amount_by_awa_fyb'] - 2,
        gross_outlay_amount_by_pro_cpe=af_dict['gross_outlay_amount_by_awa_cpe'] - 2,
        obligations_incurred_by_pr_cpe=af_dict['obligations_incurred_byawa_cpe'] - 2,
        ussgl487100_downward_adjus_cpe=af_dict['ussgl487100_downward_adjus_cpe'] + 2,
        ussgl497100_downward_adjus_cpe=af_dict['ussgl497100_downward_adjus_cpe'] + 2,
        ussgl487200_downward_adjus_cpe=af_dict['ussgl487200_downward_adjus_cpe'] + 2,
        ussgl497200_downward_adjus_cpe=af_dict['ussgl497200_downward_adjus_cpe'] + 2,
        deobligations_recov_by_pro_cpe=af_dict['deobligations_recov_by_awa_cpe'] + 2,
        tas=af_dict['tas'],
        object_class=af_dict['object_class'],
        by_direct_reimbursable_fun=af_dict['by_direct_reimbursable_fun'],
        submission_id=af_dict['submission_id']
    )

    op4 = ObjectClassProgramActivityFactory(
        ussgl480100_undelivered_or_fyb=af_dict['ussgl480100_undelivered_or_fyb'] - 2,
        ussgl480100_undelivered_or_cpe=af_dict['ussgl480100_undelivered_or_cpe'] - 2,
        ussgl483100_undelivered_or_cpe=af_dict['ussgl483100_undelivered_or_cpe'] - 2,
        ussgl488100_upward_adjustm_cpe=af_dict['ussgl488100_upward_adjustm_cpe'] - 2,
        obligations_undelivered_or_fyb=af_dict['obligations_undelivered_or_fyb'] - 2,
        obligations_undelivered_or_cpe=af_dict['obligations_undelivered_or_cpe'] - 2,
        ussgl490100_delivered_orde_fyb=af_dict['ussgl490100_delivered_orde_fyb'] - 2,
        ussgl490100_delivered_orde_cpe=af_dict['ussgl490100_delivered_orde_cpe'] - 2,
        ussgl493100_delivered_orde_cpe=af_dict['ussgl493100_delivered_orde_cpe'] - 2,
        ussgl498100_upward_adjustm_cpe=af_dict['ussgl498100_upward_adjustm_cpe'] - 2,
        obligations_delivered_orde_fyb=af_dict['obligations_delivered_orde_fyb'] - 2,
        obligations_delivered_orde_cpe=af_dict['obligations_delivered_orde_cpe'] - 2,
        ussgl480200_undelivered_or_fyb=af_dict['ussgl480200_undelivered_or_fyb'] - 2,
        ussgl480200_undelivered_or_cpe=af_dict['ussgl480200_undelivered_or_cpe'] - 2,
        ussgl483200_undelivered_or_cpe=af_dict['ussgl483200_undelivered_or_cpe'] - 2,
        ussgl488200_upward_adjustm_cpe=af_dict['ussgl488200_upward_adjustm_cpe'] - 2,
        gross_outlays_undelivered_fyb=af_dict['gross_outlays_undelivered_fyb'] - 2,
        gross_outlays_undelivered_cpe=af_dict['gross_outlays_undelivered_cpe'] - 2,
        ussgl490200_delivered_orde_cpe=af_dict['ussgl490200_delivered_orde_cpe'] - 2,
        ussgl490800_authority_outl_fyb=af_dict['ussgl490800_authority_outl_fyb'] - 2,
        ussgl490800_authority_outl_cpe=af_dict['ussgl490800_authority_outl_cpe'] - 2,
        ussgl498200_upward_adjustm_cpe=af_dict['ussgl498200_upward_adjustm_cpe'] - 2,
        gross_outlays_delivered_or_fyb=af_dict['gross_outlays_delivered_or_fyb'] - 2,
        gross_outlays_delivered_or_cpe=af_dict['gross_outlays_delivered_or_cpe'] - 2,
        gross_outlay_amount_by_pro_fyb=af_dict['gross_outlay_amount_by_awa_fyb'] - 2,
        gross_outlay_amount_by_pro_cpe=af_dict['gross_outlay_amount_by_awa_cpe'] - 2,
        obligations_incurred_by_pr_cpe=af_dict['obligations_incurred_byawa_cpe'] - 2,
        ussgl487100_downward_adjus_cpe=af_dict['ussgl487100_downward_adjus_cpe'] + 2,
        ussgl497100_downward_adjus_cpe=af_dict['ussgl497100_downward_adjus_cpe'] + 2,
        ussgl487200_downward_adjus_cpe=af_dict['ussgl487200_downward_adjus_cpe'] + 2,
        ussgl497200_downward_adjus_cpe=af_dict['ussgl497200_downward_adjus_cpe'] + 2,
        deobligations_recov_by_pro_cpe=af_dict['deobligations_recov_by_awa_cpe'] + 2,
        tas=af_dict['tas'],
        object_class='some-other-class',
        by_direct_reimbursable_fun='some-other-dr',
        submission_id=af_dict['submission_id']
    )

    errors = number_of_errors(_FILE, database, models=[af1, af2, op1, op2, op3, op4])
    assert errors == 0


def test_failure(database):
    """
        Tests failing that each USSGL account balance or subtotal, when totaled by combination of TAS, object class
        code, and direct/reimbursable flag provided in File C, should be a subset of, or equal to, the same combinations
        in File B
    """
    af1 = AwardFinancialFactory(**af_dict)

    op1 = ObjectClassProgramActivityFactory(
        ussgl480100_undelivered_or_fyb=af_dict['ussgl480100_undelivered_or_fyb'] + 1,
        ussgl480100_undelivered_or_cpe=af_dict['ussgl480100_undelivered_or_cpe'] + 1,
        ussgl483100_undelivered_or_cpe=af_dict['ussgl483100_undelivered_or_cpe'] + 1,
        ussgl488100_upward_adjustm_cpe=af_dict['ussgl488100_upward_adjustm_cpe'] + 1,
        obligations_undelivered_or_fyb=af_dict['obligations_undelivered_or_fyb'] + 1,
        obligations_undelivered_or_cpe=af_dict['obligations_undelivered_or_cpe'] + 1,
        ussgl490100_delivered_orde_fyb=af_dict['ussgl490100_delivered_orde_fyb'] + 1,
        ussgl490100_delivered_orde_cpe=af_dict['ussgl490100_delivered_orde_cpe'] + 1,
        ussgl493100_delivered_orde_cpe=af_dict['ussgl493100_delivered_orde_cpe'] + 1,
        ussgl498100_upward_adjustm_cpe=af_dict['ussgl498100_upward_adjustm_cpe'] + 1,
        obligations_delivered_orde_fyb=af_dict['obligations_delivered_orde_fyb'] + 1,
        obligations_delivered_orde_cpe=af_dict['obligations_delivered_orde_cpe'] + 1,
        ussgl480200_undelivered_or_fyb=af_dict['ussgl480200_undelivered_or_fyb'] + 1,
        ussgl480200_undelivered_or_cpe=af_dict['ussgl480200_undelivered_or_cpe'] + 1,
        ussgl483200_undelivered_or_cpe=af_dict['ussgl483200_undelivered_or_cpe'] + 1,
        ussgl488200_upward_adjustm_cpe=af_dict['ussgl488200_upward_adjustm_cpe'] + 1,
        gross_outlays_undelivered_fyb=af_dict['gross_outlays_undelivered_fyb'] + 1,
        gross_outlays_undelivered_cpe=af_dict['gross_outlays_undelivered_cpe'] + 1,
        ussgl490200_delivered_orde_cpe=af_dict['ussgl490200_delivered_orde_cpe'] + 1,
        ussgl490800_authority_outl_fyb=af_dict['ussgl490800_authority_outl_fyb'] + 1,
        ussgl490800_authority_outl_cpe=af_dict['ussgl490800_authority_outl_cpe'] + 1,
        ussgl498200_upward_adjustm_cpe=af_dict['ussgl498200_upward_adjustm_cpe'] + 1,
        gross_outlays_delivered_or_fyb=af_dict['gross_outlays_delivered_or_fyb'] + 1,
        gross_outlays_delivered_or_cpe=af_dict['gross_outlays_delivered_or_cpe'] + 1,
        gross_outlay_amount_by_pro_fyb=af_dict['gross_outlay_amount_by_awa_fyb'] + 1,
        gross_outlay_amount_by_pro_cpe=af_dict['gross_outlay_amount_by_awa_cpe'] + 1,
        obligations_incurred_by_pr_cpe=af_dict['obligations_incurred_byawa_cpe'] + 1,
        ussgl487100_downward_adjus_cpe=af_dict['ussgl487100_downward_adjus_cpe'] + 1,
        ussgl497100_downward_adjus_cpe=af_dict['ussgl497100_downward_adjus_cpe'] + 1,
        ussgl487200_downward_adjus_cpe=af_dict['ussgl487200_downward_adjus_cpe'] + 1,
        ussgl497200_downward_adjus_cpe=af_dict['ussgl497200_downward_adjus_cpe'] + 1,
        deobligations_recov_by_pro_cpe=af_dict['deobligations_recov_by_awa_cpe'] + 1,
        tas=af_dict['tas'],
        object_class=af_dict['object_class'],
        by_direct_reimbursable_fun=af_dict['by_direct_reimbursable_fun'],
        submission_id=af_dict['submission_id']
    )

    op2 = ObjectClassProgramActivityFactory(
        ussgl480100_undelivered_or_fyb=af_dict['ussgl480100_undelivered_or_fyb'] + 1,
        ussgl480100_undelivered_or_cpe=af_dict['ussgl480100_undelivered_or_cpe'] + 1,
        ussgl483100_undelivered_or_cpe=af_dict['ussgl483100_undelivered_or_cpe'] + 1,
        ussgl488100_upward_adjustm_cpe=af_dict['ussgl488100_upward_adjustm_cpe'] + 1,
        obligations_undelivered_or_fyb=af_dict['obligations_undelivered_or_fyb'] + 1,
        obligations_undelivered_or_cpe=af_dict['obligations_undelivered_or_cpe'] + 1,
        ussgl490100_delivered_orde_fyb=af_dict['ussgl490100_delivered_orde_fyb'] + 1,
        ussgl490100_delivered_orde_cpe=af_dict['ussgl490100_delivered_orde_cpe'] + 1,
        ussgl493100_delivered_orde_cpe=af_dict['ussgl493100_delivered_orde_cpe'] + 1,
        ussgl498100_upward_adjustm_cpe=af_dict['ussgl498100_upward_adjustm_cpe'] + 1,
        obligations_delivered_orde_fyb=af_dict['obligations_delivered_orde_fyb'] + 1,
        obligations_delivered_orde_cpe=af_dict['obligations_delivered_orde_cpe'] + 1,
        ussgl480200_undelivered_or_fyb=af_dict['ussgl480200_undelivered_or_fyb'] + 1,
        ussgl480200_undelivered_or_cpe=af_dict['ussgl480200_undelivered_or_cpe'] + 1,
        ussgl483200_undelivered_or_cpe=af_dict['ussgl483200_undelivered_or_cpe'] + 1,
        ussgl488200_upward_adjustm_cpe=af_dict['ussgl488200_upward_adjustm_cpe'] + 1,
        gross_outlays_undelivered_fyb=af_dict['gross_outlays_undelivered_fyb'] + 1,
        gross_outlays_undelivered_cpe=af_dict['gross_outlays_undelivered_cpe'] + 1,
        ussgl490200_delivered_orde_cpe=af_dict['ussgl490200_delivered_orde_cpe'] + 1,
        ussgl490800_authority_outl_fyb=af_dict['ussgl490800_authority_outl_fyb'] + 1,
        ussgl490800_authority_outl_cpe=af_dict['ussgl490800_authority_outl_cpe'] + 1,
        ussgl498200_upward_adjustm_cpe=af_dict['ussgl498200_upward_adjustm_cpe'] + 1,
        gross_outlays_delivered_or_fyb=af_dict['gross_outlays_delivered_or_fyb'] + 1,
        gross_outlays_delivered_or_cpe=af_dict['gross_outlays_delivered_or_cpe'] + 1,
        gross_outlay_amount_by_pro_fyb=af_dict['gross_outlay_amount_by_awa_fyb'] + 1,
        gross_outlay_amount_by_pro_cpe=af_dict['gross_outlay_amount_by_awa_cpe'] + 1,
        obligations_incurred_by_pr_cpe=af_dict['obligations_incurred_byawa_cpe'] + 1,
        ussgl487100_downward_adjus_cpe=af_dict['ussgl487100_downward_adjus_cpe'] + 1,
        ussgl497100_downward_adjus_cpe=af_dict['ussgl497100_downward_adjus_cpe'] + 1,
        ussgl487200_downward_adjus_cpe=af_dict['ussgl487200_downward_adjus_cpe'] + 1,
        ussgl497200_downward_adjus_cpe=af_dict['ussgl497200_downward_adjus_cpe'] + 1,
        deobligations_recov_by_pro_cpe=af_dict['deobligations_recov_by_awa_cpe'] + 1,
        tas='some-other-tas',
        object_class=af_dict['object_class'],
        by_direct_reimbursable_fun=af_dict['by_direct_reimbursable_fun'],
        submission_id=af_dict['submission_id']
    )

    op3 = ObjectClassProgramActivityFactory(
        ussgl480100_undelivered_or_fyb=af_dict['ussgl480100_undelivered_or_fyb'] + 1,
        ussgl480100_undelivered_or_cpe=af_dict['ussgl480100_undelivered_or_cpe'] + 1,
        ussgl483100_undelivered_or_cpe=af_dict['ussgl483100_undelivered_or_cpe'] + 1,
        ussgl488100_upward_adjustm_cpe=af_dict['ussgl488100_upward_adjustm_cpe'] + 1,
        obligations_undelivered_or_fyb=af_dict['obligations_undelivered_or_fyb'] + 1,
        obligations_undelivered_or_cpe=af_dict['obligations_undelivered_or_cpe'] + 1,
        ussgl490100_delivered_orde_fyb=af_dict['ussgl490100_delivered_orde_fyb'] + 1,
        ussgl490100_delivered_orde_cpe=af_dict['ussgl490100_delivered_orde_cpe'] + 1,
        ussgl493100_delivered_orde_cpe=af_dict['ussgl493100_delivered_orde_cpe'] + 1,
        ussgl498100_upward_adjustm_cpe=af_dict['ussgl498100_upward_adjustm_cpe'] + 1,
        obligations_delivered_orde_fyb=af_dict['obligations_delivered_orde_fyb'] + 1,
        obligations_delivered_orde_cpe=af_dict['obligations_delivered_orde_cpe'] + 1,
        ussgl480200_undelivered_or_fyb=af_dict['ussgl480200_undelivered_or_fyb'] + 1,
        ussgl480200_undelivered_or_cpe=af_dict['ussgl480200_undelivered_or_cpe'] + 1,
        ussgl483200_undelivered_or_cpe=af_dict['ussgl483200_undelivered_or_cpe'] + 1,
        ussgl488200_upward_adjustm_cpe=af_dict['ussgl488200_upward_adjustm_cpe'] + 1,
        gross_outlays_undelivered_fyb=af_dict['gross_outlays_undelivered_fyb'] + 1,
        gross_outlays_undelivered_cpe=af_dict['gross_outlays_undelivered_cpe'] + 1,
        ussgl490200_delivered_orde_cpe=af_dict['ussgl490200_delivered_orde_cpe'] + 1,
        ussgl490800_authority_outl_fyb=af_dict['ussgl490800_authority_outl_fyb'] + 1,
        ussgl490800_authority_outl_cpe=af_dict['ussgl490800_authority_outl_cpe'] + 1,
        ussgl498200_upward_adjustm_cpe=af_dict['ussgl498200_upward_adjustm_cpe'] + 1,
        gross_outlays_delivered_or_fyb=af_dict['gross_outlays_delivered_or_fyb'] + 1,
        gross_outlays_delivered_or_cpe=af_dict['gross_outlays_delivered_or_cpe'] + 1,
        gross_outlay_amount_by_pro_fyb=af_dict['gross_outlay_amount_by_awa_fyb'] + 1,
        gross_outlay_amount_by_pro_cpe=af_dict['gross_outlay_amount_by_awa_cpe'] + 1,
        obligations_incurred_by_pr_cpe=af_dict['obligations_incurred_byawa_cpe'] + 1,
        ussgl487100_downward_adjus_cpe=af_dict['ussgl487100_downward_adjus_cpe'] + 1,
        ussgl497100_downward_adjus_cpe=af_dict['ussgl497100_downward_adjus_cpe'] + 1,
        ussgl487200_downward_adjus_cpe=af_dict['ussgl487200_downward_adjus_cpe'] + 1,
        ussgl497200_downward_adjus_cpe=af_dict['ussgl497200_downward_adjus_cpe'] + 1,
        deobligations_recov_by_pro_cpe=af_dict['deobligations_recov_by_awa_cpe'] + 1,
        tas=af_dict['tas'],
        object_class='some-other-class',
        by_direct_reimbursable_fun=af_dict['by_direct_reimbursable_fun'],
        submission_id=af_dict['submission_id']
    )

    op4 = ObjectClassProgramActivityFactory(
        ussgl480100_undelivered_or_fyb=af_dict['ussgl480100_undelivered_or_fyb'] + 1,
        ussgl480100_undelivered_or_cpe=af_dict['ussgl480100_undelivered_or_cpe'] + 1,
        ussgl483100_undelivered_or_cpe=af_dict['ussgl483100_undelivered_or_cpe'] + 1,
        ussgl488100_upward_adjustm_cpe=af_dict['ussgl488100_upward_adjustm_cpe'] + 1,
        obligations_undelivered_or_fyb=af_dict['obligations_undelivered_or_fyb'] + 1,
        obligations_undelivered_or_cpe=af_dict['obligations_undelivered_or_cpe'] + 1,
        ussgl490100_delivered_orde_fyb=af_dict['ussgl490100_delivered_orde_fyb'] + 1,
        ussgl490100_delivered_orde_cpe=af_dict['ussgl490100_delivered_orde_cpe'] + 1,
        ussgl493100_delivered_orde_cpe=af_dict['ussgl493100_delivered_orde_cpe'] + 1,
        ussgl498100_upward_adjustm_cpe=af_dict['ussgl498100_upward_adjustm_cpe'] + 1,
        obligations_delivered_orde_fyb=af_dict['obligations_delivered_orde_fyb'] + 1,
        obligations_delivered_orde_cpe=af_dict['obligations_delivered_orde_cpe'] + 1,
        ussgl480200_undelivered_or_fyb=af_dict['ussgl480200_undelivered_or_fyb'] + 1,
        ussgl480200_undelivered_or_cpe=af_dict['ussgl480200_undelivered_or_cpe'] + 1,
        ussgl483200_undelivered_or_cpe=af_dict['ussgl483200_undelivered_or_cpe'] + 1,
        ussgl488200_upward_adjustm_cpe=af_dict['ussgl488200_upward_adjustm_cpe'] + 1,
        gross_outlays_undelivered_fyb=af_dict['gross_outlays_undelivered_fyb'] + 1,
        gross_outlays_undelivered_cpe=af_dict['gross_outlays_undelivered_cpe'] + 1,
        ussgl490200_delivered_orde_cpe=af_dict['ussgl490200_delivered_orde_cpe'] + 1,
        ussgl490800_authority_outl_fyb=af_dict['ussgl490800_authority_outl_fyb'] + 1,
        ussgl490800_authority_outl_cpe=af_dict['ussgl490800_authority_outl_cpe'] + 1,
        ussgl498200_upward_adjustm_cpe=af_dict['ussgl498200_upward_adjustm_cpe'] + 1,
        gross_outlays_delivered_or_fyb=af_dict['gross_outlays_delivered_or_fyb'] + 1,
        gross_outlays_delivered_or_cpe=af_dict['gross_outlays_delivered_or_cpe'] + 1,
        gross_outlay_amount_by_pro_fyb=af_dict['gross_outlay_amount_by_awa_fyb'] + 1,
        gross_outlay_amount_by_pro_cpe=af_dict['gross_outlay_amount_by_awa_cpe'] + 1,
        obligations_incurred_by_pr_cpe=af_dict['obligations_incurred_byawa_cpe'] + 1,
        ussgl487100_downward_adjus_cpe=af_dict['ussgl487100_downward_adjus_cpe'] + 1,
        ussgl497100_downward_adjus_cpe=af_dict['ussgl497100_downward_adjus_cpe'] + 1,
        ussgl487200_downward_adjus_cpe=af_dict['ussgl487200_downward_adjus_cpe'] + 1,
        ussgl497200_downward_adjus_cpe=af_dict['ussgl497200_downward_adjus_cpe'] + 1,
        deobligations_recov_by_pro_cpe=af_dict['deobligations_recov_by_awa_cpe'] + 1,
        tas=af_dict['tas'],
        object_class=af_dict['other-class'],
        by_direct_reimbursable_fun='some-other-dr',
        submission_id=af_dict['submission_id']
    )

    errors = number_of_errors(_FILE, database, models=[af1, op1, op2, op3, op4])
    assert errors == 1
