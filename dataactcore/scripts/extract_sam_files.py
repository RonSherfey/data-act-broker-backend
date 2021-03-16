import argparse
import logging
import os
import re
import tempfile
import boto3

from dataactcore.logging import configure_logging
from dataactcore.config import CONFIG_BROKER
from dataactcore.utils.duns import get_client, REMOTE_SAM_DUNS_DIR, REMOTE_SAM_EXEC_COMP_DIR
from dataactvalidator.health_check import create_app

logger = logging.getLogger(__name__)


def process_sam_dir(bucket, ssh_key=None):
    """ Processes through SAMs SFTP servers and copies their files to an S3 bucket

        Args:
            bucket: the bucket to copy to
            ssh_key: URI to ssh key used to pull exec comp files from SAM
    """
    root_dir = tempfile.gettempdir()
    client = get_client(ssh_key=ssh_key)
    sftp = client.open_sftp()
    # dirlist on remote host
    sam_dir = REMOTE_SAM_DUNS_DIR if ssh_key is None else REMOTE_SAM_EXEC_COMP_DIR
    dirlist = sftp.listdir(sam_dir)
    logger.info('ALL FILES IN THE BUCKET')
    logger.info([filename for filename in dirlist])

    # generate chronological list of daily and monthly files
    sorted_monthly_file_names = sorted([monthly_file for monthly_file in dirlist if re.match('.*MONTHLY_V2_\d+\.ZIP',
                                                                                             monthly_file.upper())])
    sorted_daily_file_names = sorted([daily_file for daily_file in dirlist if re.match('.*DAILY_V2_\d+\.ZIP',
                                                                                       daily_file.upper())])

    # load in earliest monthly file for historic
    copy_from_dir(root_dir, sorted_monthly_file_names[0], bucket, sftp=sftp, ssh_key=ssh_key)

    # load daily files
    for daily_file in sorted_daily_file_names:
        copy_from_dir(root_dir, daily_file, bucket, sftp=sftp, ssh_key=ssh_key, sam_dir=sam_dir)


def copy_from_dir(root_dir, file_name, bucket, sftp=None, ssh_key=None, sam_dir=REMOTE_SAM_DUNS_DIR):
    """ Process the SAM file found remotely

        Args:
            root_dir: the folder containing the SAM file
            file_name: the name of the SAM file
            bucket: the bucket to copy to
            sftp: the sftp client to pull the CSV from
            ssh_key: URI to ssh key used to pull exec comp files from SAM
            sam_dir: the remote directory to pull from
    """
    file_path = os.path.join(root_dir, file_name)
    logger.info("Pulling {}".format(file_name))
    with open(file_path, 'wb') as zip_file:
        try:
            sftp.getfo(''.join([sam_dir, '/', file_name]), zip_file)
        except Exception:
            logger.debug("Socket closed. Reconnecting...")
            ssh_client = get_client(ssh_key=ssh_key)
            sftp = ssh_client.open_sftp()
            sftp.getfo(''.join([sam_dir, '/', file_name]), zip_file)

    region_name = CONFIG_BROKER['aws_region']
    s3 = boto3.client('s3', region_name=region_name)
    dir_name = 'DUNS' if ssh_key is None else 'Executive Compensation'
    key_name = os.path.join(dir_name, file_name)
    logger.info("Copying to {}/{}".format(bucket, key_name))
    s3.upload_file(file_path, bucket, key_name)
    os.remove(file_path)


def get_parser():
    """ Generates list of command-line arguments

        Returns:
            argument parser to be used for commandline
    """
    parser = argparse.ArgumentParser(description='Copy DUNS and Exec Comp files from SAM to a S3 bucket')
    parser.add_argument('-b', '--bucket', type=str, required=True, help='The S3 bucket to copy to')
    parser.add_argument('-k', '--ssh_key', type=str, default=None, help='Private key used to access the exec comp')
    return parser


if __name__ == '__main__':
    configure_logging()
    parser = get_parser()
    args = parser.parse_args()

    bucket = args.bucket
    ssh_key = args.ssh_key

    with create_app().app_context():
        process_sam_dir(bucket)
        process_sam_dir(bucket, ssh_key)

