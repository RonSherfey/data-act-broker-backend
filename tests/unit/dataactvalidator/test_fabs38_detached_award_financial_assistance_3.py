from tests.unit.dataactcore.factories.staging import DetachedAwardFinancialAssistanceFactory
from tests.unit.dataactvalidator.utils import number_of_errors, query_columns

_FILE = 'fabs38_detached_award_financial_assistance_3'


def test_column_headers(database):
    expected_subset = {'row_number', 'awarding_office_code', 'action_type', 'correction_delete_indicatr', 'action_date',
                       'uniqueid_AssistanceTransactionUniqueKey'}
    actual = set(query_columns(_FILE, database))
    assert expected_subset == actual


def test_success(database):
    """ Test AwardingOfficeCode must be submitted for new awards (ActionType = A) or mixed aggregate records
        (ActionType = E) whose ActionDate is on or after October 1, 2018, and whose CorrectionDeleteIndicator is either
        Blank or C.
    """

    # All factors as stated
    det_award_1 = DetachedAwardFinancialAssistanceFactory(awarding_office_code='AAAAAA', action_type='A',
                                                          action_date='10/01/2018', correction_delete_indicatr='')
    det_award_2 = DetachedAwardFinancialAssistanceFactory(awarding_office_code='111111', action_type='e',
                                                          action_date='10/01/2018', correction_delete_indicatr='C')

    # Rule ignored for earlier dates
    det_award_3 = DetachedAwardFinancialAssistanceFactory(awarding_office_code='', action_type='E',
                                                          action_date='10/01/2017', correction_delete_indicatr='C')

    # Rule ignored for other action types
    det_award_4 = DetachedAwardFinancialAssistanceFactory(awarding_office_code=None, action_type='B',
                                                          action_date='10/01/2018', correction_delete_indicatr='')

    # Rule ignored for CorrectionDeleteIndicator of D
    det_award_5 = DetachedAwardFinancialAssistanceFactory(awarding_office_code=None, action_type='A',
                                                          action_date='10/01/2018', correction_delete_indicatr='D')

    # Rule ignored for action type is None
    det_award_6 = DetachedAwardFinancialAssistanceFactory(awarding_office_code='', action_type=None,
                                                          action_date='10/01/2018', correction_delete_indicatr='')
    det_award_7 = DetachedAwardFinancialAssistanceFactory(awarding_office_code=None, action_type=None,
                                                          action_date='10/02/2018', correction_delete_indicatr='C')

    errors = number_of_errors(_FILE, database, models=[det_award_1, det_award_2, det_award_3, det_award_4, det_award_5,
                                                       det_award_6, det_award_7])
    assert errors == 0


def test_failure(database):
    """ Test failure AwardingOfficeCode must be submitted for new awards (ActionType = A) or mixed aggregate records
        (ActionType = E) whose ActionDate is on or after October 1, 2018, and whose CorrectionDeleteIndicator is either
        Blank or C.
    """

    det_award_1 = DetachedAwardFinancialAssistanceFactory(awarding_office_code='', action_type='A',
                                                          action_date='10/01/2018', correction_delete_indicatr='')
    det_award_2 = DetachedAwardFinancialAssistanceFactory(awarding_office_code=None, action_type='e',
                                                          action_date='10/02/2018', correction_delete_indicatr='C')
    errors = number_of_errors(_FILE, database, models=[det_award_1, det_award_2])
    assert errors == 2
