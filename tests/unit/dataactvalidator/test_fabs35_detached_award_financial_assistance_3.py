from tests.unit.dataactcore.factories.staging import DetachedAwardFinancialAssistanceFactory
from tests.unit.dataactcore.factories.domain import ZipsFactory
from tests.unit.dataactvalidator.utils import number_of_errors, query_columns

_FILE = 'fabs35_detached_award_financial_assistance_3'


def test_column_headers(database):
    expected_subset = {'row_number', 'legal_entity_zip5', 'legal_entity_zip_last4',
                       'uniqueid_AssistanceTransactionUniqueKey'}
    actual = set(query_columns(_FILE, database))
    assert expected_subset == actual


def test_success(database):
    """ LegalEntityZIP5 + LegalEntityZIPLast4 is not a valid 9 digit zip. Null/blank zip codes ignored. """
    zip_1 = ZipsFactory(zip5='12345', zip_last4='6789')
    det_award_1 = DetachedAwardFinancialAssistanceFactory(legal_entity_zip5='12345', legal_entity_zip_last4='6789',
                                                          correction_delete_indicatr='')
    det_award_2 = DetachedAwardFinancialAssistanceFactory(legal_entity_zip5='12345', legal_entity_zip_last4=None,
                                                          correction_delete_indicatr=None)
    det_award_3 = DetachedAwardFinancialAssistanceFactory(legal_entity_zip5=None, legal_entity_zip_last4='6789',
                                                          correction_delete_indicatr='c')
    det_award_4 = DetachedAwardFinancialAssistanceFactory(legal_entity_zip5='12345', legal_entity_zip_last4='',
                                                          correction_delete_indicatr='C')
    det_award_5 = DetachedAwardFinancialAssistanceFactory(legal_entity_zip5='', legal_entity_zip_last4='6789',
                                                          correction_delete_indicatr='')

    # half bad code but other half blank ignored
    det_award_6 = DetachedAwardFinancialAssistanceFactory(legal_entity_zip5='', legal_entity_zip_last4='9876',
                                                          correction_delete_indicatr='')
    det_award_7 = DetachedAwardFinancialAssistanceFactory(legal_entity_zip5='54321', legal_entity_zip_last4='',
                                                          correction_delete_indicatr='')

    # Ignore correction delete indicator of D
    det_award_8 = DetachedAwardFinancialAssistanceFactory(legal_entity_zip5='12345', legal_entity_zip_last4='9876',
                                                          correction_delete_indicatr='d')

    errors = number_of_errors(_FILE, database, models=[zip_1, det_award_1, det_award_2, det_award_3, det_award_4,
                                                       det_award_5, det_award_6, det_award_7, det_award_8])
    assert errors == 0


def test_failure(database):
    """ LegalEntityZIP5 is not a valid zip code. """
    zip_1 = ZipsFactory(zip5='12345', zip_last4='6789')
    det_award_1 = DetachedAwardFinancialAssistanceFactory(legal_entity_zip5='12345', legal_entity_zip_last4='9876',
                                                          correction_delete_indicatr='')

    errors = number_of_errors(_FILE, database, models=[zip_1, det_award_1])
    assert errors == 1
