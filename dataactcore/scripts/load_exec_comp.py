import logging
import os
import re
import argparse
import datetime
import json
import tempfile

from dataactcore.models.domainModels import DUNS
from dataactcore.interfaces.db import GlobalDB
from dataactcore.logging import configure_logging
from dataactvalidator.health_check import create_app
from dataactcore.utils.duns import get_client, REMOTE_SAM_EXEC_COMP_DIR, parse_exec_comp_file, update_exec_comp_duns

logger = logging.getLogger(__name__)


def process_exec_comp_dir(sess, historic, local, ssh_key, benchmarks=None, metrics=None, reload_date=None):
    """ Process the script arguments to figure out which files to process in which order

        Args:
            sess: the database connection
            historic: whether to load in monthly file and daily files after, or just the latest daily files
            local: path to local directory to process, if None, it will go though the remote SAM service
            ssh_key: URI to ssh key used to pull exec comp files from SAM
            benchmarks: whether to log times
            metrics: dictionary representing metrics data for the load
            reload_date: specific date to force reload from
    """
    if not metrics:
        metrics = {}

    sftp = None

    # dealing with a local or remote directory
    if not (local or ssh_key) or (local and ssh_key):
        raise Exception('Please provide the local param or the ssh key.')
    if ssh_key:
        root_dir = tempfile.gettempdir()
        client = get_client(ssh_key=ssh_key)
        sftp = client.open_sftp()
        # dirlist on remote host
        dirlist = sftp.listdir(REMOTE_SAM_EXEC_COMP_DIR)
    elif local:
        root_dir = local
        dirlist = os.listdir(local)

    # generate chronological list of daily and monthly files
    sorted_monthly_file_names = sorted([monthly_file for monthly_file in dirlist if re.match('.*MONTHLY_\d+\.ZIP',
                                                                                             monthly_file.upper())])
    sorted_daily_file_names = sorted([daily_file for daily_file in dirlist if re.match('.*DAILY_\d+\.ZIP',
                                                                                       daily_file.upper())])

    # load in earliest monthly file for historic
    if historic and sorted_monthly_file_names:
        process_from_dir(root_dir, sorted_monthly_file_names[0], sess, sftp=sftp, ssh_key=ssh_key, metrics=metrics,
                         monthly=True)

    # load in daily files after depending on params
    if sorted_daily_file_names:
        # determine which daily files to load
        earliest_daily_file = None
        if historic and sorted_monthly_file_names:
            earliest_daily_file = sorted_monthly_file_names[0].replace("MONTHLY", "DAILY")
        elif not historic:
            # if update, make sure it's been done once before
            if reload_date:
                # a bit redundant but also date validation
                load_date = datetime.datetime.strptime(reload_date, '%Y-%m-%d')
            else:
                load_date = sess.query(DUNS.last_exec_comp_mod_date). \
                    order_by(DUNS.last_exec_comp_mod_date.desc()). \
                    filter(DUNS.last_exec_comp_mod_date.isnot(None)). \
                    first()
                load_date = load_date[0]
                if not load_date:
                    raise Exception('No last executive compenstation mod date found in database. '
                                    'Please run historic loader first.')
            load_date = load_date.strftime("%Y%m%d")

            earliest_daily_file = re.sub("_DAILY_[0-9]{8}\.ZIP", "_DAILY_" + load_date + ".ZIP",
                                         sorted_daily_file_names[0])
        daily_files_after = sorted_daily_file_names
        if earliest_daily_file:
            sorted_full_list = sorted(sorted_daily_file_names + [earliest_daily_file])
            daily_files_after = sorted_full_list[sorted_full_list.index(earliest_daily_file) + 1:]

        # load daily files
        for daily_file in daily_files_after:
            process_from_dir(root_dir, daily_file, sess, sftp=sftp, ssh_key=ssh_key, metrics=metrics)


def process_from_dir(root_dir, file_name, sess, sftp=None, ssh_key=None, metrics=None, monthly=False):
    """ Process the SAM file found locally or remotely

        Args:
            root_dir: the folder containing the SAM file
            file_name: the name of the SAM file
            sess: the database connection
            sftp: the sftp client to pull the CSV from
            metrics: dictionary representing metrics data for the load
            monthly: whether it's a monthly file
    """
    if not metrics:
        metrics = {}

    file_path = os.path.join(root_dir, file_name)
    if sftp:
        logger.info("Pulling {}".format(file_name))
        with open(file_path, 'wb') as zip_file:
            try:
                sftp.getfo(''.join([REMOTE_SAM_EXEC_COMP_DIR, '/', file_name]), zip_file)
            except Exception:
                logger.debug("Socket closed. Reconnecting...")
                ssh_client = get_client(ssh_key=ssh_key)
                sftp = ssh_client.open_sftp()
                sftp.getfo(''.join([REMOTE_SAM_EXEC_COMP_DIR, '/', file_name]), zip_file)
    exec_comp_data = parse_exec_comp_file(file_name, root_dir, sftp=sftp, ssh_key=ssh_key, metrics=metrics,
                                          monthly=monthly)
    update_exec_comp_duns(sess, exec_comp_data, metrics=metrics)
    if sftp:
        os.remove(file_path)


def get_parser():
    """ Generates list of command-line arguments

        Returns:
            argument parser to be used for commandline
    """
    parser = argparse.ArgumentParser(description='Get data from SAM and update execution_compensation table')
    scope = parser.add_mutually_exclusive_group(required=True)
    scope.add_argument('-a', '--historic', action='store_true', help='Reload from the first monthly file on')
    scope.add_argument('-u', '--update', action='store_true', help='Load daily files since latest last_sam_mod_date')
    environ = parser.add_mutually_exclusive_group(required=True)
    environ.add_argument('-l', '--local', type=str, default=None, help='Local directory to work from')
    environ.add_argument('-k', '--ssh_key', type=str, default=None, help='Private key used to access the API remotely')
    parser.add_argument("-f", "--reload_date", type=str, default=None, help='Force update from a specific date'
                                                                             ' (YYYY-MM-DD)')
    return parser


if __name__ == '__main__':
    now = datetime.datetime.now()

    configure_logging()
    parser = get_parser()
    args = parser.parse_args()

    historic = args.historic
    update = args.update
    local = args.local
    ssh_key = args.ssh_key
    reload_date = args.reload_date

    metrics = {
        'script_name': 'load_exec_duns.py',
        'start_time': str(now),
        'files_processed': [],
        'records_received': 0,
        'records_processed': 0,
        'updated_duns': [],
        'records_updated': 0
    }

    with create_app().app_context():
        sess = GlobalDB.db().session
        process_exec_comp_dir(sess, historic, local, ssh_key, metrics=metrics, reload_date=reload_date)
        sess.close()

    metrics['records_updated'] = len(set(metrics['updated_duns']))
    del metrics['updated_duns']

    metrics['duration'] = str(datetime.datetime.now() - now)
    with open('load_exec_comp_metrics.json', 'w+') as metrics_file:
        json.dump(metrics, metrics_file)
