import datetime
import logging

from dataactcore.logging import configure_logging
from dataactcore.scripts.load_duns import download_duns
from dataactvalidator.health_check import create_app

logger = logging.getLogger(__name__)


def list_available_files(start_date):
    available_files = {
        'monthly_v1': [],
        'monthly_v2': [],
        'daily_v1': [],
        'daily_v2': []
    }
    days_to_load = [start_date + datetime.timedelta(days=i) for i in
                    range((datetime.date.today() - start_date).days + 1)]
    file_formats = {
        'monthly_v1': 'SAM_FOUO_UTF-8_MONTHLY_%Y%m%d.ZIP',
        'monthly_v2': 'SAM_FOUO_UTF-8_MONTHLY_V2_%Y%m%d.ZIP',
        'daily_v1': 'SAM_FOUO_UTF-8_DAILY_%Y%m%d.ZIP',
        'daily_v2': 'SAM_FOUO_UTF-8_DAILY_V2_%Y%m%d.ZIP'
    }
    for day_to_load in days_to_load:
        logger.info('DAY: {}'.format(day_to_load.strftime('%Y-%m-%d')))
        for file_type, file_name_format in file_formats.items():
            file_name = day_to_load.strftime(file_name_format)
            try:
                download_duns(None, file_name, download=False)
                logger.info('{} - ✅'.format(file_type))
                available_files[file_type].append(file_name)
            except FileNotFoundError:
                logger.info('{} - ❌'.format(file_type))
    logger.info('Available files via SAM HTTP API')
    logger.info(available_files)


if __name__ == '__main__':
    configure_logging()

    with create_app().app_context():
        START_DATE = datetime.date(year=2014, month=1, day=1)
        list_available_files(START_DATE)
