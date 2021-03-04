import datetime
import logging
import argparse

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

def get_parser():
    """ Generates list of command-line arguments

        Returns:
            argument parser to be used for commandline
    """
    parser = argparse.ArgumentParser(description='Get data from SAM and update duns table')
    parser.add_argument("-d", "--start_date", type=str, required=True,
                        help='The first day to start checking files (YYYY-MM-DD)')
    return parser


if __name__ == '__main__':
    now = datetime.datetime.now()

    configure_logging()
    parser = get_parser()
    args = parser.parse_args()


    with create_app().app_context():
        start_date = datetime.datetime.strptime(args.start_date, '%Y-%m-%d').date()
        list_available_files(start_date)
