from tests.unit.dataactcore.factories.domain import OfficeFactory
from tests.unit.dataactcore.factories.staging import DetachedAwardFinancialAssistanceFactory
from tests.unit.dataactvalidator.utils import number_of_errors, query_columns

_FILE = 'fabs38_detached_award_financial_assistance_4_1'


def test_column_headers(database):
    expected_subset = {'row_number', 'awarding_office_code', 'uniqueid_AssistanceTransactionUniqueKey'}
    actual = set(query_columns(_FILE, database))
    assert expected_subset == actual


def test_success(database):
    """ Test when provided, AwardingOfficeCode must be a valid value from the Federal Hierarchy, including being
        designated specifically as an Assistance/Grant Office in the hierarchy.
    """

    office = OfficeFactory(office_code='12345a', financial_assistance_awards_office=True)
    det_award_1 = DetachedAwardFinancialAssistanceFactory(awarding_office_code='12345a', correction_delete_indicatr='')
    # test ignore case
    det_award_2 = DetachedAwardFinancialAssistanceFactory(awarding_office_code='12345A', correction_delete_indicatr='c')
    det_award_3 = DetachedAwardFinancialAssistanceFactory(awarding_office_code='', correction_delete_indicatr=None)
    det_award_4 = DetachedAwardFinancialAssistanceFactory(awarding_office_code=None, correction_delete_indicatr='C')
    # Ignore correction delete indicator of D
    det_award_5 = DetachedAwardFinancialAssistanceFactory(awarding_office_code='12345', correction_delete_indicatr='d')
    errors = number_of_errors(_FILE, database, models=[office, det_award_1, det_award_2, det_award_3, det_award_4,
                                                       det_award_5])
    assert errors == 0


def test_failure(database):
    """ Test fail when provided, AwardingOfficeCode must be a valid value from the Federal Hierarchy, including being
        designated specifically as an Assistance/Grant Office in the hierarchy.
    """

    office_1 = OfficeFactory(office_code='123456', financial_assistance_awards_office=True)
    office_2 = OfficeFactory(office_code='987654', financial_assistance_awards_office=False)
    det_award_1 = DetachedAwardFinancialAssistanceFactory(awarding_office_code='12345', correction_delete_indicatr=None)
    det_award_2 = DetachedAwardFinancialAssistanceFactory(awarding_office_code='1234567', correction_delete_indicatr='')
    # Test fail if grant office is false even if code matches
    det_award_3 = DetachedAwardFinancialAssistanceFactory(awarding_office_code='987654', correction_delete_indicatr='c')
    errors = number_of_errors(_FILE, database, models=[office_1, office_2, det_award_1, det_award_2, det_award_3])
    assert errors == 3
