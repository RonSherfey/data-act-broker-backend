from tests.unit.dataactcore.factories.staging import DetachedAwardFinancialAssistanceFactory
from dataactcore.models.domainModels import DUNS
from tests.unit.dataactvalidator.utils import number_of_errors, query_columns

_FILE = 'fabs31_detached_award_financial_assistance_5'


def test_column_headers(database):
    expected_subset = {'row_number', 'assistance_type', 'action_date', 'action_type', 'awardee_or_recipient_uniqu',
                       'business_types', 'record_type', 'correction_delete_indicatr',
                       'uniqueid_AssistanceTransactionUniqueKey'}
    actual = set(query_columns(_FILE, database))
    assert expected_subset == actual


def test_pubished_date_success(database):
    """ For AssistanceType of 02, 03, 04, or 05 whose ActionDate is after October 1, 2010 and ActionType = A,
        AwardeeOrRecipientUniqueIdentifier must be active as of the ActionDate,
        unless the record is an aggregate or PII-redacted non-aggregate record (RecordType=1 or 3) or individual
        recipient (BusinessTypes includes 'P'). This is an error because CorrectionDeleteIndicator is not C or the
        action date is after January 1, 2017.
    """
    duns_1 = DUNS(awardee_or_recipient_uniqu='111111111', registration_date='06/21/2017',
                  expiration_date='06/21/2018')
    det_award_1 = DetachedAwardFinancialAssistanceFactory(awardee_or_recipient_uniqu='111111111', action_type='a',
                                                          assistance_type='02', action_date='06/22/2017',
                                                          record_type=2, business_types='a',
                                                          correction_delete_indicatr='')
    # Different assistant type
    det_award_2 = DetachedAwardFinancialAssistanceFactory(awardee_or_recipient_uniqu='111111111', action_type='A',
                                                          assistance_type='01', action_date='06/20/2017',
                                                          record_type=2, business_types='A',
                                                          correction_delete_indicatr='')
    # Before October 1, 2010
    det_award_3 = DetachedAwardFinancialAssistanceFactory(awardee_or_recipient_uniqu='111111111', action_type='a',
                                                          assistance_type='02', action_date='09/30/2010',
                                                          record_type=2, business_types='A',
                                                          correction_delete_indicatr=None)
    # Handled by d31_1
    det_award_4 = DetachedAwardFinancialAssistanceFactory(awardee_or_recipient_uniqu='111111111', action_type='A',
                                                          assistance_type='03', action_date='06/20/2017',
                                                          record_type=1, business_types='A',
                                                          correction_delete_indicatr=None)
    det_award_5 = DetachedAwardFinancialAssistanceFactory(awardee_or_recipient_uniqu='111111111', action_type='A',
                                                          assistance_type='03', action_date='06/20/2017',
                                                          record_type=3, business_types='A',
                                                          correction_delete_indicatr='')
    det_award_6 = DetachedAwardFinancialAssistanceFactory(awardee_or_recipient_uniqu='111111111', action_type='a',
                                                          assistance_type='04', action_date='06/20/2017',
                                                          record_type=2, business_types='P',
                                                          correction_delete_indicatr='')
    # Handled by d31_2
    det_award_7 = DetachedAwardFinancialAssistanceFactory(awardee_or_recipient_uniqu='', action_type='A',
                                                          assistance_type='05', action_date='06/20/2017',
                                                          record_type=2, business_types='A',
                                                          correction_delete_indicatr='')
    det_award_8 = DetachedAwardFinancialAssistanceFactory(awardee_or_recipient_uniqu=None, action_type='A',
                                                          assistance_type='02', action_date='06/20/2017',
                                                          record_type=2, business_types='a',
                                                          correction_delete_indicatr='')
    # Handled by d31_3
    det_award_9 = DetachedAwardFinancialAssistanceFactory(awardee_or_recipient_uniqu='ABCDEFGHI', action_type='a',
                                                          assistance_type='03', action_date='06/20/2017',
                                                          record_type=2, business_types='A',
                                                          correction_delete_indicatr='')
    # Handled by d31_4
    det_award_10 = DetachedAwardFinancialAssistanceFactory(awardee_or_recipient_uniqu='111111112', action_type='A',
                                                           assistance_type='04', action_date='06/20/2017',
                                                           record_type=2, business_types='A',
                                                           correction_delete_indicatr='')
    # Handled by d31_6
    det_award_11 = DetachedAwardFinancialAssistanceFactory(awardee_or_recipient_uniqu='111111111', action_type='a',
                                                           assistance_type='05', action_date='06/20/2010',
                                                           record_type=2, business_types='A',
                                                           correction_delete_indicatr='c')
    # handled in d31_7
    det_award_12 = DetachedAwardFinancialAssistanceFactory(awardee_or_recipient_uniqu='111111111', action_type='B',
                                                           assistance_type='02', action_date='06/20/2017',
                                                           record_type=2, business_types='A',
                                                           correction_delete_indicatr=None)
    # handled in d4
    det_award_13 = DetachedAwardFinancialAssistanceFactory(awardee_or_recipient_uniqu='111111111', action_type='A',
                                                           assistance_type='03', action_date='YYYYMMDD',
                                                           record_type=2, business_types='a',
                                                           correction_delete_indicatr='')
    det_award_14 = DetachedAwardFinancialAssistanceFactory(awardee_or_recipient_uniqu='111111111', action_type='a',
                                                           assistance_type='04', action_date='AAAAAAAAAA',
                                                           record_type=2, business_types='A',
                                                           correction_delete_indicatr='')
    # Ignore correction delete indicator of D
    det_award_15 = DetachedAwardFinancialAssistanceFactory(assistance_type='02', action_date='06/20/2017',
                                                           awardee_or_recipient_uniqu='111111111', action_type='A',
                                                           record_type=2, business_types='a',
                                                           correction_delete_indicatr='d')

    errors = number_of_errors(_FILE, database, models=[duns_1, det_award_1, det_award_2, det_award_3, det_award_4,
                                                       det_award_5, det_award_6, det_award_7, det_award_8, det_award_9,
                                                       det_award_10, det_award_11, det_award_12, det_award_13,
                                                       det_award_14, det_award_15])
    assert errors == 0


def test_pubished_date_failure(database):
    """ Test failure for For AssistanceType of 02, 03, 04, or 05 whose ActionDate is after October 1, 2010
        and ActionType = A, AwardeeOrRecipientUniqueIdentifier must be active as of the ActionDate,
        unless the record is an aggregate or PII-redacted non-aggregate record (RecordType=1 or 3) or individual
        recipient (BusinessTypes includes 'P'). This is an error because CorrectionDeleteIndicator is not C or the
        action date is after January 1, 2017.
    """

    duns_1 = DUNS(awardee_or_recipient_uniqu='111111111', registration_date='06/21/2017',
                  expiration_date='06/21/2018')
    det_award_1 = DetachedAwardFinancialAssistanceFactory(assistance_type='02', action_date='06/20/2017',
                                                          awardee_or_recipient_uniqu='111111111', action_type='A',
                                                          record_type=2, business_types='a',
                                                          correction_delete_indicatr='')
    det_award_2 = DetachedAwardFinancialAssistanceFactory(assistance_type='03', action_date='06/22/2018',
                                                          awardee_or_recipient_uniqu='111111111', action_type='a',
                                                          record_type=2, business_types='A',
                                                          correction_delete_indicatr='')
    det_award_3 = DetachedAwardFinancialAssistanceFactory(assistance_type='04', action_date='06/22/2018',
                                                          awardee_or_recipient_uniqu='111111111', action_type='A',
                                                          record_type=2, business_types='a',
                                                          correction_delete_indicatr=None)
    det_award_4 = DetachedAwardFinancialAssistanceFactory(assistance_type='05', action_date='06/22/2018',
                                                          awardee_or_recipient_uniqu='111111111', action_type='a',
                                                          record_type=2, business_types='A',
                                                          correction_delete_indicatr='')
    # Handled by d31_6
    det_award_5 = DetachedAwardFinancialAssistanceFactory(assistance_type='05', action_date='06/22/2018',
                                                          awardee_or_recipient_uniqu='111111111', action_type='A',
                                                          record_type=2, business_types='A',
                                                          correction_delete_indicatr='C')
    det_award_6 = DetachedAwardFinancialAssistanceFactory(assistance_type='05', action_date='06/22/2018',
                                                          awardee_or_recipient_uniqu='111111111', action_type='a',
                                                          record_type=2, business_types='A',
                                                          correction_delete_indicatr='')

    errors = number_of_errors(_FILE, database, models=[duns_1, det_award_1, det_award_2, det_award_3,
                                                       det_award_4, det_award_5, det_award_6])
    assert errors == 6
