import argparse
import datetime
import logging
import os
import re
import json
import tempfile

from dataactcore.interfaces.db import GlobalDB
from dataactcore.logging import configure_logging
from dataactcore.models.domainModels import DUNS
from dataactcore.utils.parentDuns import update_missing_parent_names
from dataactcore.utils.duns import get_client, parse_duns_file, update_duns, REMOTE_SAM_DUNS_DIR
from dataactvalidator.health_check import create_app

logger = logging.getLogger(__name__)


def process_duns_dir(sess, historic, local, benchmarks=None, metrics=None, force_reload=None):
    """ Process the script arguments to figure out which files to process in which order

        Args:
            sess: the database connection
            historic: whether to load in monthly file and daily files after, or just the latest daily files
            local: path to local directory to process, if None, it will go though the remote SAM service
            benchmarks: whether to log times
            metrics: dictionary representing metrics data for the load
            force_reload: specific date to force reload from
    """
    if not metrics:
        metrics = {}

    updated_date = datetime.date.today()

    # dealing with a local or remote directory
    sftp = None
    if not local:
        root_dir = tempfile.gettempdir()
        client = get_client()
        sftp = client.open_sftp()
        # dirlist on remote host
        dirlist = sftp.listdir(REMOTE_SAM_DUNS_DIR)
    elif local:
        root_dir = local
        dirlist = os.listdir(local)

    # generate chronological list of daily and monthly files
    sorted_monthly_file_names = sorted([monthly_file for monthly_file in dirlist if re.match(".*MONTHLY_\d+\.ZIP",
                                                                                             monthly_file.upper())])
    sorted_daily_file_names = sorted([daily_file for daily_file in dirlist if re.match(".*DAILY_\d+\.ZIP",
                                                                                       daily_file.upper())])

    # load in earliest monthly file for historic
    if historic and sorted_monthly_file_names:
        process_from_dir(root_dir, sorted_monthly_file_names[0], sess, sftp, monthly=True, benchmarks=benchmarks,
                         metrics=metrics)

    # load in daily files after depending on params
    if sorted_daily_file_names:
        # determine which daily files to load
        earliest_daily_file = None
        if historic and sorted_monthly_file_names:
            earliest_daily_file = sorted_monthly_file_names[0].replace("MONTHLY", "DAILY")
        elif not historic:
            # if update, make sure it's been done once before
            if force_reload:
                # a bit redundant but also date validation
                load_date = datetime.datetime.strptime(force_reload, '%Y-%m-%d')
            else:
                load_date = sess.query(DUNS.last_sam_mod_date). \
                    order_by(DUNS.last_sam_mod_date.desc()). \
                    filter(DUNS.last_sam_mod_date.isnot(None)). \
                    first()
                load_date = load_date[0]
                if not load_date:
                    raise Exception('No last sam mod date found in DUNS table. Please run historic loader first.')
            load_date = load_date.strftime("%Y%m%d")

            earliest_daily_file = re.sub("_DAILY_[0-9]{8}\.ZIP", "_DAILY_" + load_date + ".ZIP",
                                         sorted_daily_file_names[0])
        daily_files_after = sorted_daily_file_names
        if earliest_daily_file:
            sorted_full_list = sorted(sorted_daily_file_names + [earliest_daily_file])
            daily_files_after = sorted_full_list[sorted_full_list.index(earliest_daily_file) + 1:]

        # load daily files
        for daily_file in daily_files_after:
            process_from_dir(root_dir, daily_file, sess, sftp, benchmarks=benchmarks, metrics=metrics)
        if daily_files_after:
            metrics['parent_rows_updated'] = update_missing_parent_names(sess, updated_date=updated_date)
            metrics['parent_update_date'] = str(updated_date)


def process_from_dir(root_dir, file_name, sess, sftp=None, monthly=False, benchmarks=False, metrics=None):
    """ Process the SAM file found locally or remotely

        Args:
            root_dir: the folder containing the SAM file
            file_name: the name of the SAM file
            sess: the database connection
            sftp: the sftp client to pull the CSV from
            monthly: whether it's a monthly file
            benchmarks: whether to log times
            metrics: dictionary representing metrics data for the load
    """
    if not metrics:
        metrics = {}

    file_path = os.path.join(root_dir, file_name)
    if sftp:
        logger.info("Pulling {}".format(file_name))
        with open(file_path, "wb") as zip_file:
            try:
                sftp.getfo(''.join([REMOTE_SAM_DUNS_DIR, '/', file_name]), zip_file)
            except Exception:
                logger.debug("Socket closed. Reconnecting...")
                ssh_client = get_client()
                sftp = ssh_client.open_sftp()
                sftp.getfo(''.join([REMOTE_SAM_DUNS_DIR, '/', file_name]), zip_file)
    add_update_data, delete_data = parse_duns_file(file_path, sess, monthly=monthly, benchmarks=benchmarks,
                                                   metrics=metrics)
    if add_update_data is not None:
        update_duns(sess, add_update_data, metrics=metrics)
    if delete_data is not None:
        update_duns(sess, delete_data, metrics=metrics, deletes=True)
    if sftp:
        os.remove(file_path)


def get_parser():
    """ Generates list of command-line arguments

        Returns:
            argument parser to be used for commandline
    """
    parser = argparse.ArgumentParser(description='Get data from SAM and update duns table')
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument("-a", "--historic", action="store_true", help='Reload from the first monthly file on')
    scope.add_argument("-u", "--update", action="store_true", help='Load daily files since latest last_sam_mod_date')
    environ = parser.add_mutually_exclusive_group(required=True)
    environ.add_argument("-l", "--local", type=str, default=None, help='Local directory to work from')
    environ.add_argument("-r", "--remote", action="store_true", help='Work from a remote directory (SAM)')
    parser.add_argument("-f", "--force_reload", type=str, default=None, help='Force update from a specific date'
                                                                             ' (YYYY-MM-DD)')
    parser.add_argument("-b", "--benchmarks", action="store_true", help='log times of operations for testing')
    return parser


if __name__ == '__main__':
    now = datetime.datetime.now()

    configure_logging()
    parser = get_parser()
    args = parser.parse_args()

    historic = args.historic
    update = args.update
    local = args.local
    remote = args.remote
    benchmarks = args.benchmarks
    force_reload = args.force_reload

    metrics = {
        'script_name': 'load_duns.py',
        'start_time': str(now),
        'files_processed': [],
        'records_received': 0,
        'records_processed': 0,
        'adds_received': 0,
        'updates_received': 0,
        'deletes_received': 0,
        'added_duns': [],
        'updated_duns': [],
        'records_added': 0,
        'records_updated': 0,
        'parent_rows_updated': 0,
        'parent_update_date': None
    }

    with create_app().app_context():
        sess = GlobalDB.db().session
        process_duns_dir(sess, historic, local, benchmarks=benchmarks, metrics=metrics, force_reload=force_reload)
        sess.close()

    metrics['records_added'] = len(set(metrics['added_duns']))
    metrics['records_updated'] = len(set(metrics['updated_duns']) - set(metrics['added_duns']))
    del metrics['added_duns']
    del metrics['updated_duns']

    logger.info('Added {} records and updated {} records'.format(metrics['records_added'], metrics['records_updated']))

    metrics['duration'] = str(datetime.datetime.now() - now)
    with open('load_duns_metrics.json', 'w+') as metrics_file:
        json.dump(metrics, metrics_file)
