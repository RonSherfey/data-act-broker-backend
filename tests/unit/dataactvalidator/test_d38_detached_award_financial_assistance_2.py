from tests.unit.dataactcore.factories.staging import DetachedAwardFinancialAssistanceFactory
from dataactcore.models.domainModels import Zips
from tests.unit.dataactvalidator.utils import number_of_errors, query_columns

_FILE = 'd38_detached_award_financial_assistance_2'


def test_column_headers(database):
    expected_subset = {"row_number", "place_of_performance_code"}
    actual = set(query_columns(_FILE, database))
    assert expected_subset == actual


def test_success(database):
    """ PrimaryPlaceOfPerformanceCode last three digits must be a valid county code when format is XX**###. """

    zip_code = Zips(zip5="12345", county_number="123")
    det_award_1 = DetachedAwardFinancialAssistanceFactory(place_of_performance_code="NY*****")
    det_award_2 = DetachedAwardFinancialAssistanceFactory(place_of_performance_code="00FO333")
    det_award_3 = DetachedAwardFinancialAssistanceFactory(place_of_performance_code="NY**123")
    errors = number_of_errors(_FILE, database, models=[det_award_1, det_award_2, det_award_3, zip_code])
    assert errors == 0


def test_failure(database):
    """ Test failure for PrimaryPlaceOfPerformanceCode last three digits must be a valid county code when
        format is XX**###. """

    zip_code = Zips(zip5="12345", county_number="123")
    det_award_1 = DetachedAwardFinancialAssistanceFactory(place_of_performance_code="00**333")
    det_award_2 = DetachedAwardFinancialAssistanceFactory(place_of_performance_code="00**33")
    errors = number_of_errors(_FILE, database, models=[det_award_1, det_award_2, zip_code])
    assert errors == 2
