from tests.unit.dataactcore.factories.staging import DetachedAwardFinancialAssistanceFactory
from tests.unit.dataactvalidator.utils import number_of_errors, query_columns

_FILE = 'fabsreq4_detached_award_financial_assistance'


def test_column_headers(database):
    expected_subset = {'row_number', 'business_funds_indicator', 'correction_delete_indicatr',
                       'uniqueid_AssistanceTransactionUniqueKey'}
    actual = set(query_columns(_FILE, database))
    assert expected_subset == actual


def test_success(database):
    """ Test BusinessFundsIndicator is required for all submissions except delete records. """

    det_award = DetachedAwardFinancialAssistanceFactory(correction_delete_indicatr='C', business_funds_indicator='REC')
    det_award_2 = DetachedAwardFinancialAssistanceFactory(correction_delete_indicatr='', business_funds_indicator='NON')
    # Test ignoring for D records
    det_award_3 = DetachedAwardFinancialAssistanceFactory(correction_delete_indicatr='d', business_funds_indicator=None)
    det_award_4 = DetachedAwardFinancialAssistanceFactory(correction_delete_indicatr='D', business_funds_indicator='')
    det_award_5 = DetachedAwardFinancialAssistanceFactory(correction_delete_indicatr='D', business_funds_indicator='RE')

    errors = number_of_errors(_FILE, database, models=[det_award, det_award_2, det_award_3, det_award_4, det_award_5])
    assert errors == 0


def test_failure(database):
    """ Test fail BusinessFundsIndicator is required for all submissions except delete records. """

    det_award = DetachedAwardFinancialAssistanceFactory(correction_delete_indicatr='c', business_funds_indicator=None)
    det_award_2 = DetachedAwardFinancialAssistanceFactory(correction_delete_indicatr=None, business_funds_indicator='')

    errors = number_of_errors(_FILE, database, models=[det_award, det_award_2])
    assert errors == 2
