from random import randint

from tests.unit.dataactcore.factories.domain import TASFactory
from tests.unit.dataactcore.factories.staging import AppropriationFactory, ObjectClassProgramActivityFactory
from tests.unit.dataactvalidator.utils import number_of_errors, query_columns


_FILE = 'a19_cross_file'


def test_column_headers(database):
    expected_subset = {'source_row_number', 'source_value_obligations_incurred_total_cpe',
                       'target_value_obligations_incurred_by_pr_cpe_sum', 'difference', 'uniqueid_TAS'}
    actual = set(query_columns(_FILE, database))
    assert (actual & expected_subset) == expected_subset


def test_sum_matches(database):
    tas = TASFactory()
    database.session.add(tas)
    database.session.flush()

    op1 = ObjectClassProgramActivityFactory(account_num=tas.account_num)
    op2 = ObjectClassProgramActivityFactory(account_num=tas.account_num)
    approp_val = -sum(op.obligations_incurred_by_pr_cpe for op in (op1, op2))
    approp = AppropriationFactory(account_num=tas.account_num, obligations_incurred_total_cpe=approp_val)
    assert number_of_errors(_FILE, database, models=[approp, op1, op2]) == 0


def test_sum_does_not_match(database):
    tas = TASFactory()
    database.session.add(tas)
    database.session.flush()

    op1 = ObjectClassProgramActivityFactory(account_num=tas.account_num)
    op2 = ObjectClassProgramActivityFactory(account_num=tas.account_num)
    approp_val = -sum(op.obligations_incurred_by_pr_cpe for op in (op1, op2))
    approp_val += randint(1, 9999)  # different value now
    approp = AppropriationFactory(account_num=tas.account_num, obligations_incurred_total_cpe=approp_val)
    assert number_of_errors(_FILE, database, models=[approp, op1, op2]) == 1
