import logging

from dataactbroker.helpers import generation_helper, generic_helper

from dataactcore.interfaces.db import GlobalDB
from dataactcore.interfaces.function_bag import mark_job_status
from dataactcore.models import lookups
from dataactcore.models.jobModels import Job
from dataactcore.utils.jsonResponse import JsonResponse
from dataactcore.utils.responseException import ResponseException
from dataactcore.utils.statusCode import StatusCode
from dataactcore.utils.stringCleaner import StringCleaner

logger = logging.getLogger(__name__)


def generate_file(submission, file_type, start, end, agency_type):
    """ Start a file generation job for the specified file type within a submission

        Args:
            submission: submission for which we're generating the file
            file_type: type of file to generate the job for
            start: the start date for the file to generate
            end: the end date for the file to generate
            agency_type: The type of agency (awarding or funding) to generate the file for (only used for D file
                generation)

        Returns:
            Results of check_generation or JsonResponse object containing an error if the prerequisite job isn't
            complete.
    """
    error_message = None
    # submission is a FABS submission
    if submission.d2_submission:
        error_message = "Cannot generate files for FABS submissions."

    elif file_type in ['D1', 'D2']:
        # D file generation requires start and end date
        if not start or not end:
            error_message = "Must have a start and end date for D file generation."
        # D files can only be generated by awarding or funding agency
        elif agency_type not in ['awarding', 'funding']:
            error_message = "agency_type must be either awarding or funding for D file generation."

    # Only D1, D2, E, and F files can be generated
    elif file_type not in ['E', 'F']:
        error_message = "File type must be either D1, D2, E, or F"

    # Return any client errors
    if error_message:
        return JsonResponse.error(ValueError(error_message), StatusCode.CLIENT_ERROR)

    sess = GlobalDB.db().session
    job = sess.query(Job).filter(Job.submission_id == submission.submission_id,
                                 Job.file_type_id == lookups.FILE_TYPE_DICT_LETTER_ID[file_type],
                                 Job.job_type_id == lookups.JOB_TYPE_DICT['file_upload']).one()
    logger.info({
        'message': 'Starting {} file generation within submission {}'.format(file_type, submission.submission_id),
        'message_type': 'BrokerInfo',
        'submission_id': submission.submission_id,
        'job_id': job.job_id,
        'file_type': file_type
    })

    # Check prerequisites on upload job
    if not generation_helper.check_generation_prereqs(submission.submission_id, file_type):
        return JsonResponse.error(ResponseException("Must wait for completion of prerequisite validation job",
                                                    StatusCode.CLIENT_ERROR), StatusCode.CLIENT_ERROR)
    try:
        if file_type in ['D1', 'D2']:
            generation_helper.start_d_generation(job, start, end, agency_type)
        else:
            generation_helper.start_e_f_generation(job)
    except Exception as e:
        mark_job_status(job.job_id, 'failed')
        job.error_message = str(e)
        sess.commit()
        return JsonResponse.error(e, StatusCode.INTERNAL_ERROR)

    # Return same response as check generation route
    return check_generation(submission, file_type)


def check_generation(submission, file_type):
    """ Return information about file generation jobs connected to a submission

        Args:
            submission: submission to get information from
            file_type: type of file being generated to check on

        Returns:
            Response object with keys status, file_type, url, message.
            If file_type is D1 or D2, also includes start and end.
    """
    sess = GlobalDB.db().session
    upload_job = sess.query(Job).filter(Job.submission_id == submission.submission_id,
                                        Job.file_type_id == lookups.FILE_TYPE_DICT_LETTER_ID[file_type],
                                        Job.job_type_id == lookups.JOB_TYPE_DICT['file_upload']).one()

    response_dict = generation_helper.check_file_generation(upload_job.job_id)

    return JsonResponse.create(StatusCode.OK, response_dict)


def generate_detached_file(file_type, cgac_code, frec_code, start_date, end_date, quarter, agency_type):
    """ Start a file generation job for the specified file type not connected to a submission

        Args:
            file_type: type of file to be generated
            cgac_code: the code of a CGAC agency if generating for a CGAC agency
            frec_code: the code of a FREC agency if generating for a FREC agency
            start_date: start date in a string, formatted MM/DD/YYYY
            end_date: end date in a string, formatted MM/DD/YYYY
            quarter: quarter to generate for, formatted Q#/YYYY
            agency_type: The type of agency (awarding or funding) to generate the file for

        Returns:
            JSONResponse object with keys job_id, status, file_type, url, message, start_date, and end_date.

        Raises:
            ResponseException: if the start_date and end_date Strings cannot be parsed into dates
    """
    # Make sure it's a valid request
    if not cgac_code and not frec_code:
        return JsonResponse.error(ValueError("Detached file generation requires CGAC or FR Entity Code"),
                                  StatusCode.CLIENT_ERROR)

    if file_type in ['D1', 'D2']:
        # Make sure we have a start and end date for D1/D2 generation
        if not start_date or not end_date:
            return JsonResponse.error(ValueError("Must have a start and end date for D file generation."),
                                      StatusCode.CLIENT_ERROR)

        # Check if date format is MM/DD/YYYY
        if not (StringCleaner.is_date(start_date) and StringCleaner.is_date(end_date)):
            raise ResponseException('Start or end date cannot be parsed into a date', StatusCode.CLIENT_ERROR)

        if agency_type not in ('awarding', 'funding'):
            return JsonResponse.error(ValueError("agency_type must be either awarding or funding."),
                                      StatusCode.CLIENT_ERROR)
    else:
        # Check if date format is Q#/YYYY
        if not quarter:
            return JsonResponse.error(ValueError("Must have a quarter for A file generation."), StatusCode.CLIENT_ERROR)

        try:
            start_date, end_date = generic_helper.quarter_to_dates(quarter)
        except ResponseException as e:
            return JsonResponse.error(e, StatusCode.CLIENT_ERROR)

    # Add job info
    file_type_name = lookups.FILE_TYPE_DICT_LETTER_NAME[file_type]
    new_job = generation_helper.create_generation_job(file_type_name, start_date, end_date)

    agency_code = frec_code if frec_code else cgac_code
    logger.info({'message': 'Starting detached {} file generation'.format(file_type), 'message_type': 'BrokerInfo',
                 'job_id': new_job.job_id, 'file_type': file_type, 'agency_code': agency_code, 'start_date': start_date,
                 'end_date': end_date})

    try:
        if file_type in ['D1', 'D2']:
            generation_helper.start_d_generation(new_job, start_date, end_date, agency_type, agency_code=agency_code)
        else:
            generation_helper.start_a_generation(new_job, start_date, end_date, agency_code)
    except Exception as e:
        mark_job_status(new_job.job_id, 'failed')
        new_job.error_message = str(e)
        GlobalDB.db().session.commit()
        return JsonResponse.error(e, StatusCode.INTERNAL_ERROR)

    # Return same response as check generation route
    return check_detached_generation(new_job.job_id)


def check_detached_generation(job_id):
    """ Return information about detached file generation jobs

        Args:
            job_id: ID of the detached generation job

        Returns:
            Response object with keys job_id, status, file_type, url, message, start, and end.
    """
    response_dict = generation_helper.check_file_generation(job_id)

    return JsonResponse.create(StatusCode.OK, response_dict)
