import logging

from dataactcore.interfaces.db import GlobalDB
from dataactcore.logging import configure_logging

from dataactvalidator.health_check import create_app

logger = logging.getLogger(__name__)

BACKFILL_DISPLAYTAS_SF133_SQL = """
    UPDATE sf_133
    SET display_tas =
        CONCAT_WS(
            '-',
            allocation_transfer_agency,
            agency_identifier,
            CASE WHEN availability_type_code IS NOT NULL AND availability_type_code <> '' THEN availability_type_code
                ELSE CONCAT_WS('/', beginning_period_of_availa, ending_period_of_availabil)
                END,
            main_account_code,
            sub_account_code
        )
    WHERE display_tas IS NULL;
"""

if __name__ == '__main__':
    configure_logging()

    with create_app().app_context():
        sess = GlobalDB.db().session

        logger.info('Backfilling empty display_tas values in the sf_133 table.')
        executed = sess.execute(BACKFILL_DISPLAYTAS_SF133_SQL)
        sess.commit()

        logger.info('Backfill completed, {} rows affected\n'.format(executed.rowcount))

        sess.close()
