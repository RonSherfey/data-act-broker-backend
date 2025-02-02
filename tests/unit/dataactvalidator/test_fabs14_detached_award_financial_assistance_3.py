from tests.unit.dataactcore.factories.staging import DetachedAwardFinancialAssistanceFactory
from tests.unit.dataactvalidator.utils import number_of_errors, query_columns

_FILE = 'fabs14_detached_award_financial_assistance_3'


def test_column_headers(database):
    expected_subset = {'row_number', 'legal_entity_country_code', 'record_type', 'legal_entity_zip_last4',
                       'uniqueid_AssistanceTransactionUniqueKey'}
    actual = set(query_columns(_FILE, database))
    assert expected_subset == actual


def test_success(database):
    """ Test LegalEntityZIPLast4 is required for domestic recipients (i.e., when LegalEntityCountryCode = USA)
        for non-aggregate records (i.e., when RecordType = 2) record type 1 and non-USA don't affect success
    """
    det_award = DetachedAwardFinancialAssistanceFactory(legal_entity_country_code='USA', record_type=2,
                                                        legal_entity_zip_last4='12345', correction_delete_indicatr='')
    det_award_2 = DetachedAwardFinancialAssistanceFactory(legal_entity_country_code='USA', record_type=1,
                                                          legal_entity_zip_last4=None, correction_delete_indicatr=None)
    det_award_null = DetachedAwardFinancialAssistanceFactory(legal_entity_country_code='UK', record_type=2,
                                                             legal_entity_zip_last4='', correction_delete_indicatr='c')
    # Ignore correction delete indicator of D
    det_award_3 = DetachedAwardFinancialAssistanceFactory(legal_entity_country_code='USA', record_type=2,
                                                          legal_entity_zip_last4='', correction_delete_indicatr='d')

    errors = number_of_errors(_FILE, database, models=[det_award, det_award_2, det_award_3, det_award_null])
    assert errors == 0


def test_failure(database):
    """ Test failure when LegalEntityZIPLast4 is blank for domestic recipients for non-aggregate records """

    det_award = DetachedAwardFinancialAssistanceFactory(legal_entity_country_code='USA', record_type=2,
                                                        legal_entity_zip_last4=None, correction_delete_indicatr='')
    det_award_2 = DetachedAwardFinancialAssistanceFactory(legal_entity_country_code='USA', record_type=2,
                                                          legal_entity_zip_last4='', correction_delete_indicatr='c')
    det_award_3 = DetachedAwardFinancialAssistanceFactory(legal_entity_country_code='UsA', record_type=2,
                                                          legal_entity_zip_last4='', correction_delete_indicatr=None)

    errors = number_of_errors(_FILE, database, models=[det_award, det_award_2, det_award_3])
    assert errors == 3
