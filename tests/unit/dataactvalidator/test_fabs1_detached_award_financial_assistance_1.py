from tests.unit.dataactcore.factories.staging import DetachedAwardFinancialAssistanceFactory
from tests.unit.dataactvalidator.utils import number_of_errors, query_columns

_FILE = 'fabs1_detached_award_financial_assistance_1'


def test_column_headers(database):
    expected_subset = {'row_number', 'record_type', 'fain', 'uniqueid_AssistanceTransactionUniqueKey'}
    actual = set(query_columns(_FILE, database))
    assert expected_subset == actual


def test_success(database):
    """ Test that record_type 1 doesn't affect success (can have no FAIN) and that FAIN works where it's needed. """
    det_award = DetachedAwardFinancialAssistanceFactory(record_type=1, fain='17TCEP0034', correction_delete_indicatr='')
    det_award_2 = DetachedAwardFinancialAssistanceFactory(record_type=2, fain='17TCEP0034',
                                                          correction_delete_indicatr='C')
    det_award_3 = DetachedAwardFinancialAssistanceFactory(record_type=3, fain='17TCEP0034',
                                                          correction_delete_indicatr=None)
    det_award_null = DetachedAwardFinancialAssistanceFactory(record_type=1, fain=None, correction_delete_indicatr='c')
    # Ignore correction delete indicator of D
    det_award_4 = DetachedAwardFinancialAssistanceFactory(record_type=2, fain=None, correction_delete_indicatr='d')

    errors = number_of_errors(_FILE, database, models=[det_award, det_award_2, det_award_3, det_award_4,
                                                       det_award_null])
    assert errors == 0


def test_failure(database):
    """ Test that a null FAIN with record type 2 or 3 returns an error. """

    det_award = DetachedAwardFinancialAssistanceFactory(record_type=2, fain=None, correction_delete_indicatr=None)
    det_award_2 = DetachedAwardFinancialAssistanceFactory(record_type=3, fain='', correction_delete_indicatr='C')

    errors = number_of_errors(_FILE, database, models=[det_award, det_award_2])
    assert errors == 2
