from tests.unit.dataactcore.factories.staging import DetachedAwardFinancialAssistanceFactory
from tests.unit.dataactvalidator.utils import number_of_errors, query_columns

_FILE = 'fabs9_detached_award_financial_assistance_2'


def test_column_headers(database):
    expected_subset = {'row_number', 'record_type', 'awardee_or_recipient_legal',
                       'uniqueid_AssistanceTransactionUniqueKey'}
    actual = set(query_columns(_FILE, database))
    assert expected_subset == actual


def test_success(database):
    """ Test that awardee_or_recipient_legal contains "REDACTED DUE TO PII" for record type 3 and record types 1 and
        2 don't affect success.
    """
    det_award = DetachedAwardFinancialAssistanceFactory(record_type=3, awardee_or_recipient_legal='REDACTEd DUE TO PII',
                                                        correction_delete_indicatr='')
    det_award_2 = DetachedAwardFinancialAssistanceFactory(record_type=2, awardee_or_recipient_legal='TEST AGENCY',
                                                          correction_delete_indicatr=None)
    det_award_3 = DetachedAwardFinancialAssistanceFactory(record_type=1, awardee_or_recipient_legal='TEST AGENCY 2',
                                                          correction_delete_indicatr='c')
    # Ignore correction delete indicator of D
    det_award_4 = DetachedAwardFinancialAssistanceFactory(record_type=3,
                                                          awardee_or_recipient_legal='REDACTED DUE TO PI',
                                                          correction_delete_indicatr='d')

    errors = number_of_errors(_FILE, database, models=[det_award, det_award_2, det_award_3, det_award_4])
    assert errors == 0


def test_failure(database):
    """ Test that awardee_or_recipient_legal without "REDACTED DUE TO PII" for record type 3 fails. """

    det_award = DetachedAwardFinancialAssistanceFactory(record_type=3,
                                                        awardee_or_recipient_legal='REDACTED DUE TO PI',
                                                        correction_delete_indicatr='')
    det_award_2 = DetachedAwardFinancialAssistanceFactory(record_type=3, awardee_or_recipient_legal='other',
                                                          correction_delete_indicatr='C')

    errors = number_of_errors(_FILE, database, models=[det_award, det_award_2])
    assert errors == 2
