import datetime
import pytest
import json

from flask import Flask, g
from unittest.mock import Mock

from dataactbroker.handlers import fileHandler
from dataactbroker.handlers.submission_handler import (certify_dabs_submission, get_submission_metadata,
                                                       get_revalidation_threshold, get_submission_data,
                                                       move_certified_data, get_latest_certification_period,
                                                       revert_to_certified)

from dataactcore.config import CONFIG_BROKER
from dataactcore.models.lookups import (PUBLISH_STATUS_DICT, JOB_STATUS_DICT, JOB_TYPE_DICT, FILE_TYPE_DICT,
                                        FILE_STATUS_DICT)
from dataactcore.models.errorModels import ErrorMetadata, CertifiedErrorMetadata, File
from dataactcore.models.jobModels import CertifyHistory, CertifiedComment, Job, Submission, CertifiedFilesHistory
from dataactcore.models.stagingModels import (Appropriation, ObjectClassProgramActivity, AwardFinancial,
                                              CertifiedAppropriation, CertifiedObjectClassProgramActivity,
                                              CertifiedAwardFinancial, FlexField, CertifiedFlexField)
from dataactcore.utils.responseException import ResponseException

from tests.unit.dataactcore.factories.domain import CGACFactory, FRECFactory
from tests.unit.dataactcore.factories.job import (SubmissionFactory, JobFactory, CertifyHistoryFactory,
                                                  RevalidationThresholdFactory, QuarterlyRevalidationThresholdFactory,
                                                  CommentFactory)
from tests.unit.dataactcore.factories.staging import DetachedAwardFinancialAssistanceFactory
from tests.unit.dataactcore.factories.user import UserFactory


@pytest.mark.usefixtures('job_constants')
def test_get_submission_metadata_quarterly_dabs_cgac(database):
    """ Tests the get_submission_metadata function for quarterly dabs submissions """
    sess = database.session

    now = datetime.datetime.utcnow()
    now_plus_10 = now + datetime.timedelta(minutes=10)
    cgac = CGACFactory(cgac_code='001', agency_name='CGAC Agency')
    frec_cgac = CGACFactory(cgac_code='999', agency_name='FREC CGAC')
    frec = FRECFactory(frec_code='0001', agency_name='FREC Agency', cgac=frec_cgac)

    sub = SubmissionFactory(submission_id=1, created_at=now, updated_at=now_plus_10, cgac_code=cgac.cgac_code,
                            reporting_fiscal_period=3, reporting_fiscal_year=2017, is_quarter_format=True,
                            publish_status_id=PUBLISH_STATUS_DICT['updated'], d2_submission=False, number_of_errors=40,
                            number_of_warnings=200)
    # Job for submission
    job = JobFactory(submission_id=sub.submission_id, last_validated=now_plus_10,
                     job_type_id=JOB_TYPE_DICT['csv_record_validation'], job_status_id=JOB_STATUS_DICT['finished'],
                     file_type_id=FILE_TYPE_DICT['appropriations'], number_of_rows=3, file_size=7655)
    job_2 = JobFactory(submission_id=sub.submission_id, last_validated=now_plus_10,
                       job_type_id=JOB_TYPE_DICT['csv_record_validation'], job_status_id=JOB_STATUS_DICT['finished'],
                       file_type_id=FILE_TYPE_DICT['program_activity'], number_of_rows=7, file_size=12345)

    sess.add_all([cgac, frec_cgac, frec, sub, job, job_2])
    sess.commit()

    # Test for Quarterly, updated DABS cgac submission
    expected_results = {
        'cgac_code': cgac.cgac_code,
        'frec_code': None,
        'agency_name': cgac.agency_name,
        'number_of_errors': 40,
        'number_of_warnings': 200,
        'number_of_rows': 8,
        'total_size': 20000,
        'created_on': now.strftime('%m/%d/%Y'),
        'last_updated': now_plus_10.strftime('%Y-%m-%dT%H:%M:%S'),
        'last_validated': now_plus_10.strftime('%Y-%m-%dT%H:%M:%S'),
        'reporting_period': 'Q1/2017',
        'publish_status': 'updated',
        'quarterly_submission': True,
        'certified_submission': None,
        'fabs_submission': False,
        'fabs_meta': None
    }

    results = get_submission_metadata(sub)
    assert results == expected_results


@pytest.mark.usefixtures('job_constants')
def test_get_submission_metadata_quarterly_dabs_frec(database):
    """ Tests the get_submission_metadata function for quarterly dabs submissions frec """
    sess = database.session

    now = datetime.datetime.utcnow()
    frec_cgac = CGACFactory(cgac_code='999', agency_name='FREC CGAC')
    frec = FRECFactory(frec_code='0001', agency_name='FREC Agency', cgac=frec_cgac)

    sub = SubmissionFactory(submission_id=2, created_at=now, updated_at=now, cgac_code=None, frec_code=frec.frec_code,
                            reporting_fiscal_period=6, reporting_fiscal_year=2010, is_quarter_format=True,
                            publish_status_id=PUBLISH_STATUS_DICT['published'], d2_submission=False, number_of_errors=0,
                            number_of_warnings=0)

    sess.add_all([frec_cgac, frec, sub])
    sess.commit()

    expected_results = {
        'cgac_code': None,
        'frec_code': frec.frec_code,
        'agency_name': frec.agency_name,
        'number_of_errors': 0,
        'number_of_warnings': 0,
        'number_of_rows': 0,
        'total_size': 0,
        'created_on': now.strftime('%m/%d/%Y'),
        'last_updated': now.strftime('%Y-%m-%dT%H:%M:%S'),
        'last_validated': '',
        'reporting_period': 'Q2/2010',
        'publish_status': 'published',
        'quarterly_submission': True,
        'certified_submission': None,
        'fabs_submission': False,
        'fabs_meta': None
    }

    results = get_submission_metadata(sub)
    assert results == expected_results


@pytest.mark.usefixtures('job_constants')
def test_get_submission_metadata_monthly_dabs(database):
    """ Tests the get_submission_metadata function for monthly dabs submissions """
    sess = database.session

    now = datetime.datetime.utcnow()
    now_plus_10 = now + datetime.timedelta(minutes=10)
    start_date = datetime.date(2000, 1, 1)
    cgac = CGACFactory(cgac_code='001', agency_name='CGAC Agency')

    sub = SubmissionFactory(submission_id=3, created_at=now, updated_at=now_plus_10, cgac_code=cgac.cgac_code,
                            reporting_fiscal_period=4, reporting_fiscal_year=2016, is_quarter_format=False,
                            publish_status_id=PUBLISH_STATUS_DICT['unpublished'], d2_submission=False,
                            reporting_start_date=start_date, number_of_errors=20, number_of_warnings=0)

    sess.add_all([cgac, sub])
    sess.commit()

    expected_results = {
        'cgac_code': cgac.cgac_code,
        'frec_code': None,
        'agency_name': cgac.agency_name,
        'number_of_errors': 20,
        'number_of_warnings': 0,
        'number_of_rows': 0,
        'total_size': 0,
        'created_on': now.strftime('%m/%d/%Y'),
        'last_updated': now_plus_10.strftime('%Y-%m-%dT%H:%M:%S'),
        'last_validated': '',
        'reporting_period': start_date.strftime('%m/%Y'),
        'publish_status': 'unpublished',
        'quarterly_submission': False,
        'certified_submission': None,
        'fabs_submission': False,
        'fabs_meta': None
    }

    results = get_submission_metadata(sub)
    assert results == expected_results


@pytest.mark.usefixtures('job_constants')
def test_get_submission_metadata_unpublished_fabs(database):
    """ Tests the get_submission_metadata function for unpublished fabs submissions """
    sess = database.session

    now = datetime.datetime.utcnow()
    start_date = datetime.date(2000, 1, 1)
    cgac = CGACFactory(cgac_code='001', agency_name='CGAC Agency')
    frec_cgac = CGACFactory(cgac_code='999', agency_name='FREC CGAC')
    frec = FRECFactory(frec_code='0001', agency_name='FREC Agency', cgac=frec_cgac)

    sub = SubmissionFactory(submission_id=4, created_at=now, updated_at=now, cgac_code=cgac.cgac_code,
                            reporting_fiscal_period=1, reporting_fiscal_year=2015, is_quarter_format=False,
                            publish_status_id=PUBLISH_STATUS_DICT['unpublished'], d2_submission=True,
                            reporting_start_date=start_date, number_of_errors=4, number_of_warnings=1)

    sess.add_all([cgac, frec_cgac, frec, sub])
    sess.commit()

    expected_results = {
        'cgac_code': cgac.cgac_code,
        'frec_code': None,
        'agency_name': cgac.agency_name,
        'number_of_errors': 4,
        'number_of_warnings': 1,
        'number_of_rows': 0,
        'total_size': 0,
        'created_on': now.strftime('%m/%d/%Y'),
        'last_updated': now.strftime('%Y-%m-%dT%H:%M:%S'),
        'last_validated': '',
        'reporting_period': start_date.strftime('%m/%Y'),
        'publish_status': 'unpublished',
        'quarterly_submission': False,
        'certified_submission': None,
        'fabs_submission': True,
        'fabs_meta': {'publish_date': None, 'published_file': None, 'total_rows': 0, 'valid_rows': 0}
    }

    results = get_submission_metadata(sub)
    assert results == expected_results


@pytest.mark.usefixtures('job_constants')
def test_get_submission_metadata_published_fabs(database):
    """ Tests the get_submission_metadata function for published fabs submissions """
    sess = database.session

    now = datetime.datetime.utcnow()
    now_plus_10 = now + datetime.timedelta(minutes=10)
    start_date = datetime.date(2000, 1, 1)
    cgac = CGACFactory(cgac_code='001', agency_name='CGAC Agency')
    frec_cgac = CGACFactory(cgac_code='999', agency_name='FREC CGAC')
    frec = FRECFactory(frec_code='0001', agency_name='FREC Agency', cgac=frec_cgac)

    sub = SubmissionFactory(submission_id=5, created_at=now, updated_at=now, cgac_code=cgac.cgac_code,
                            reporting_fiscal_period=5, reporting_fiscal_year=2010, is_quarter_format=False,
                            publish_status_id=PUBLISH_STATUS_DICT['published'], d2_submission=True,
                            reporting_start_date=start_date, number_of_errors=0, number_of_warnings=2)
    # Data for FABS
    dafa_1 = DetachedAwardFinancialAssistanceFactory(submission_id=sub.submission_id, is_valid=True)
    dafa_2 = DetachedAwardFinancialAssistanceFactory(submission_id=sub.submission_id, is_valid=False)
    cert_hist = CertifyHistoryFactory(submission=sub, created_at=now_plus_10)

    sess.add_all([cgac, frec_cgac, frec, sub, dafa_1, dafa_2, cert_hist])
    sess.commit()

    expected_results = {
        'cgac_code': cgac.cgac_code,
        'frec_code': None,
        'agency_name': cgac.agency_name,
        'number_of_errors': 0,
        'number_of_warnings': 2,
        'number_of_rows': 0,
        'total_size': 0,
        'created_on': now.strftime('%m/%d/%Y'),
        'last_updated': now.strftime('%Y-%m-%dT%H:%M:%S'),
        'last_validated': '',
        'reporting_period': start_date.strftime('%m/%Y'),
        'publish_status': 'published',
        'quarterly_submission': False,
        'certified_submission': None,
        'fabs_submission': True,
        'fabs_meta': {
            'publish_date': now_plus_10.strftime('%-I:%M%p %m/%d/%Y'),
            'published_file': None,
            'total_rows': 2,
            'valid_rows': 1
        }
    }

    results = get_submission_metadata(sub)
    assert results == expected_results


@pytest.mark.usefixtures('job_constants')
def test_get_submission_metadata_test_submission(database):
    """ Tests the get_submission_metadata function for published fabs submissions """
    sess = database.session

    now = datetime.datetime.utcnow()
    cgac = CGACFactory(cgac_code='001', agency_name='CGAC Agency')

    sub1 = SubmissionFactory(submission_id=1, created_at=now, updated_at=now, cgac_code=cgac.cgac_code,
                             reporting_fiscal_period=3, reporting_fiscal_year=2017, is_quarter_format=True,
                             publish_status_id=PUBLISH_STATUS_DICT['updated'], d2_submission=False, number_of_errors=40,
                             number_of_warnings=200)
    sub2 = SubmissionFactory(submission_id=2, created_at=now, updated_at=now, cgac_code=cgac.cgac_code,
                             reporting_fiscal_period=3, reporting_fiscal_year=2017, is_quarter_format=True,
                             publish_status_id=PUBLISH_STATUS_DICT['unpublished'], d2_submission=False,
                             number_of_errors=40, number_of_warnings=200)

    sess.add_all([cgac, sub1, sub2])
    sess.commit()

    # Test for test submission
    expected_results = {
        'cgac_code': cgac.cgac_code,
        'frec_code': None,
        'agency_name': cgac.agency_name,
        'number_of_errors': 40,
        'number_of_warnings': 200,
        'number_of_rows': 0,
        'total_size': 0,
        'created_on': now.strftime('%m/%d/%Y'),
        'last_updated': now.strftime('%Y-%m-%dT%H:%M:%S'),
        'last_validated': '',
        'reporting_period': 'Q1/2017',
        'publish_status': 'unpublished',
        'quarterly_submission': True,
        'certified_submission': 1,
        'fabs_submission': False,
        'fabs_meta': None
    }

    results = get_submission_metadata(sub2)
    assert results == expected_results


def test_get_revalidation_threshold(database):
    """ Tests the get_revalidation_threshold function to make sure it returns the correct, properly formatted date """
    sess = database.session

    # Revalidation date
    reval = RevalidationThresholdFactory(revalidation_date=datetime.datetime(2018, 1, 15, 0, 0))

    sess.add(reval)
    sess.commit()

    results = get_revalidation_threshold()
    assert results['revalidation_threshold'] == '2018-01-15T00:00:00'


def test_get_revalidation_threshold_no_threshold():
    """ Tests the get_revalidation_threshold function to make sure it returns an empty string if there's no date """
    results = get_revalidation_threshold()
    assert results['revalidation_threshold'] == ''


def test_get_latest_certification_period(database):
    """ Tests the get_latest_certification_period function to make sure it returns the correct quarter and year """
    sess = database.session

    # Revalidation date
    today = datetime.datetime.today()
    reval1 = QuarterlyRevalidationThresholdFactory(quarter=1, year=2016, window_start=today - datetime.timedelta(1))
    reval2 = QuarterlyRevalidationThresholdFactory(quarter=2, year=2016, window_start=today)
    reval3 = QuarterlyRevalidationThresholdFactory(quarter=3, year=2017, window_start=today + datetime.timedelta(1))
    sess.add_all([reval1, reval2, reval3])
    sess.commit()

    results = get_latest_certification_period()
    assert results['quarter'] == 2
    assert results['year'] == 2016


def test_get_latest_certification_period_no_threshold():
    """ Tests the get_latest_certification_period function to make sure it returns Nones if there's no prior period """
    results = get_latest_certification_period()
    assert results['quarter'] is None
    assert results['year'] is None


@pytest.mark.usefixtures('job_constants')
def test_get_submission_data_dabs(database):
    """ Tests the get_submission_data function for dabs records """
    sess = database.session

    cgac = CGACFactory(cgac_code='001', agency_name='CGAC Agency')

    sub = SubmissionFactory(submission_id=1, d2_submission=False)
    sub_2 = SubmissionFactory(submission_id=2, d2_submission=False)

    # Job for submission
    job = JobFactory(job_id=1, submission_id=sub.submission_id, job_type_id=JOB_TYPE_DICT['csv_record_validation'],
                     job_status_id=JOB_STATUS_DICT['finished'], file_type_id=FILE_TYPE_DICT['appropriations'],
                     number_of_rows=3, file_size=7655, original_filename='file_1')
    job_2 = JobFactory(job_id=2, submission_id=sub.submission_id, job_type_id=JOB_TYPE_DICT['file_upload'],
                       job_status_id=JOB_STATUS_DICT['finished'], file_type_id=FILE_TYPE_DICT['program_activity'],
                       number_of_rows=None, file_size=None, original_filename='file_2')
    job_3 = JobFactory(job_id=3, submission_id=sub.submission_id, job_type_id=JOB_TYPE_DICT['csv_record_validation'],
                       job_status_id=JOB_STATUS_DICT['running'], file_type_id=FILE_TYPE_DICT['program_activity'],
                       number_of_rows=7, file_size=12345, original_filename='file_2')
    job_4 = JobFactory(job_id=4, submission_id=sub.submission_id, job_type_id=JOB_TYPE_DICT['validation'],
                       job_status_id=JOB_STATUS_DICT['waiting'], file_type_id=None, number_of_rows=None,
                       file_size=None, original_filename=None)
    job_5 = JobFactory(job_id=5, submission_id=sub_2.submission_id, job_type_id=JOB_TYPE_DICT['validation'],
                       job_status_id=JOB_STATUS_DICT['waiting'], file_type_id=None, number_of_rows=None,
                       file_size=None, original_filename=None)

    sess.add_all([cgac, sub, sub_2, job, job_2, job_3, job_4, job_5])
    sess.commit()

    # a basic csv_validation job, should be in results
    correct_job = {
        'job_id': job.job_id,
        'job_status': job.job_status_name,
        'job_type': job.job_type_name,
        'filename': job.original_filename,
        'file_size': job.file_size,
        'number_of_rows': job.number_of_rows - 1,
        'file_type': job.file_type_name,
        'file_status': '',
        'error_type': '',
        'error_data': [],
        'warning_data': [],
        'missing_headers': [],
        'duplicated_headers': []
    }

    # cross-file job, should be in results
    correct_cross_job = {
        'job_id': job_4.job_id,
        'job_status': job_4.job_status_name,
        'job_type': job_4.job_type_name,
        'filename': None,
        'file_size': None,
        'number_of_rows': 0,
        'file_type': '',
        'file_status': '',
        'error_type': '',
        'error_data': [],
        'warning_data': [],
        'missing_headers': [],
        'duplicated_headers': []
    }

    # upload job, shouldn't be in the results
    upload_job = {
        'job_id': job_2.job_id,
        'job_status': job_2.job_status_name,
        'job_type': job_2.job_type_name,
        'filename': job_2.original_filename,
        'file_size': job_2.file_size,
        'number_of_rows': job_2.number_of_rows,
        'file_type': job_2.file_type_name,
        'file_status': '',
        'error_type': '',
        'error_data': [],
        'warning_data': [],
        'missing_headers': [],
        'duplicated_headers': []
    }

    # cross-file job but from another submission, shouldn't be in the results
    different_sub_job = {
        'job_id': job_5.job_id,
        'job_status': job_5.job_status_name,
        'job_type': job_5.job_type_name,
        'filename': job_5.original_filename,
        'file_size': job_5.file_size,
        'number_of_rows': job_5.number_of_rows,
        'file_type': job_5.file_type_name,
        'file_status': '',
        'error_type': '',
        'error_data': [],
        'warning_data': [],
        'missing_headers': [],
        'duplicated_headers': []
    }

    response = get_submission_data(sub)
    response = json.loads(response.data.decode('UTF-8'))
    results = response['jobs']
    assert len(results) == 3
    assert correct_job in results
    assert correct_cross_job in results
    assert upload_job not in results
    assert different_sub_job not in results

    response = get_submission_data(sub, 'appropriations')
    response = json.loads(response.data.decode('UTF-8'))
    results = response['jobs']
    assert len(results) == 1
    assert results[0] == correct_job


@pytest.mark.usefixtures('job_constants')
def test_certify_dabs_submission(database, monkeypatch):
    """ Tests the certify_dabs_submission function """
    with Flask('test-app').app_context():
        now = datetime.datetime.utcnow()
        sess = database.session

        user = UserFactory()
        cgac = CGACFactory(cgac_code='001', agency_name='CGAC Agency')
        submission = SubmissionFactory(created_at=now, updated_at=now, cgac_code=cgac.cgac_code,
                                       reporting_fiscal_period=3, reporting_fiscal_year=2017, is_quarter_format=True,
                                       publishable=True, publish_status_id=PUBLISH_STATUS_DICT['unpublished'],
                                       d2_submission=False, number_of_errors=0, number_of_warnings=200,
                                       certifying_user_id=None)
        quarter_reval = QuarterlyRevalidationThresholdFactory(year=2017, quarter=1,
                                                              window_start=now - datetime.timedelta(days=1))
        sess.add_all([user, cgac, submission, quarter_reval])
        sess.commit()

        comment = CommentFactory(file_type_id=FILE_TYPE_DICT['appropriations'], comment='Test',
                                 submission_id=submission.submission_id)
        job_1 = JobFactory(submission_id=submission.submission_id, last_validated=now,
                           job_type_id=JOB_TYPE_DICT['csv_record_validation'])
        job_2 = JobFactory(submission_id=submission.submission_id, last_validated=now + datetime.timedelta(days=1),
                           job_type_id=JOB_TYPE_DICT['csv_record_validation'])
        sess.add_all([job_1, job_2, comment])
        sess.commit()

        flex_field = FlexField(file_type_id=FILE_TYPE_DICT['appropriations'], header='flex_test', job_id=job_1.job_id,
                               submission_id=submission.submission_id, row_number=2, cell=None)
        sess.add(flex_field)
        sess.commit()

        g.user = user
        file_handler = fileHandler.FileHandler({}, is_local=True)
        monkeypatch.setattr(file_handler, 'move_certified_files', Mock(return_value=True))
        monkeypatch.setattr(fileHandler.GlobalDB, 'db', Mock(return_value=database))

        certify_dabs_submission(submission, file_handler)

        sess.refresh(submission)
        certify_history = sess.query(CertifyHistory).filter_by(submission_id=submission.submission_id).one_or_none()
        assert certify_history is not None
        assert submission.certifying_user_id == user.user_id
        assert submission.publish_status_id == PUBLISH_STATUS_DICT['published']

        # Make sure certified comments are created
        certified_comment = sess.query(CertifiedComment).filter_by(submission_id=submission.submission_id).one_or_none()
        assert certified_comment is not None

        # Make sure certified flex fields are created
        certified_flex = sess.query(CertifiedFlexField).filter_by(submission_id=submission.submission_id).one_or_none()
        assert certified_flex is not None


@pytest.mark.usefixtures('job_constants')
def test_certify_dabs_submission_revalidation_needed(database):
    """ Tests the certify_dabs_submission function preventing certification when revalidation threshold isn't met """
    with Flask('test-app').app_context():
        now = datetime.datetime.utcnow()
        earlier = now - datetime.timedelta(days=1)
        sess = database.session

        user = UserFactory()
        cgac = CGACFactory(cgac_code='001', agency_name='CGAC Agency')
        submission = SubmissionFactory(created_at=earlier, updated_at=earlier, cgac_code=cgac.cgac_code,
                                       reporting_fiscal_period=3, reporting_fiscal_year=2017, is_quarter_format=True,
                                       publishable=True, publish_status_id=PUBLISH_STATUS_DICT['unpublished'],
                                       d2_submission=False, number_of_errors=0, number_of_warnings=200,
                                       certifying_user_id=None)
        reval = RevalidationThresholdFactory(revalidation_date=now)
        sess.add_all([user, cgac, submission, reval])
        sess.commit()
        job = JobFactory(submission_id=submission.submission_id, last_validated=earlier,
                         job_type_id=JOB_TYPE_DICT['csv_record_validation'])
        sess.add(job)
        sess.commit()

        g.user = user
        file_handler = fileHandler.FileHandler({}, is_local=True)
        response = certify_dabs_submission(submission, file_handler)
        response_json = json.loads(response.data.decode('UTF-8'))
        assert response.status_code == 400
        assert response_json['message'] == 'This submission has not been validated since before the revalidation ' \
                                           'threshold ({}), it must be revalidated before certifying.'. \
            format(now.strftime('%Y-%m-%d %H:%M:%S'))


@pytest.mark.usefixtures('job_constants')
def test_certify_dabs_submission_quarterly_revalidation_not_in_db(database):
    """ Tests that a DABS submission that doesnt have its year/quarter in the system won't be able to certify. """
    with Flask('test-app').app_context():
        now = datetime.datetime.utcnow()
        sess = database.session

        user = UserFactory()
        cgac = CGACFactory(cgac_code='001', agency_name='CGAC Agency')
        submission = SubmissionFactory(created_at=now, updated_at=now, cgac_code=cgac.cgac_code,
                                       reporting_fiscal_period=3, reporting_fiscal_year=2017, is_quarter_format=True,
                                       publishable=True, publish_status_id=PUBLISH_STATUS_DICT['unpublished'],
                                       d2_submission=False, number_of_errors=0, number_of_warnings=200,
                                       certifying_user_id=None)
        sess.add_all([user, cgac, submission])
        sess.commit()

        job = JobFactory(submission_id=submission.submission_id, last_validated=now,
                         job_type_id=JOB_TYPE_DICT['csv_record_validation'])
        sess.add(job)
        sess.commit()

        g.user = user
        file_handler = fileHandler.FileHandler({}, is_local=True)
        response = certify_dabs_submission(submission, file_handler)
        response_json = json.loads(response.data.decode('UTF-8'))
        assert response.status_code == 400
        assert response_json['message'] == 'No submission window for this year and quarter was found. If this is an ' \
                                           'error, please contact the Service Desk.'


@pytest.mark.usefixtures('job_constants')
def test_certify_dabs_submission_quarterly_revalidation_too_early(database):
    """ Tests that a DABS submission that was last validated before the window start cannot be certified. """
    with Flask('test-app').app_context():
        now = datetime.datetime.utcnow()
        earlier = now - datetime.timedelta(days=1)
        sess = database.session

        user = UserFactory()
        cgac = CGACFactory(cgac_code='001', agency_name='CGAC Agency')
        submission = SubmissionFactory(created_at=earlier, updated_at=earlier, cgac_code=cgac.cgac_code,
                                       reporting_fiscal_period=3, reporting_fiscal_year=2017, is_quarter_format=True,
                                       publishable=True, publish_status_id=PUBLISH_STATUS_DICT['unpublished'],
                                       d2_submission=False, number_of_errors=0, number_of_warnings=200,
                                       certifying_user_id=None)
        quarter_reval = QuarterlyRevalidationThresholdFactory(year=2017, quarter=1, window_start=now)
        sess.add_all([user, cgac, submission, quarter_reval])
        sess.commit()

        job = JobFactory(submission_id=submission.submission_id, last_validated=earlier,
                         job_type_id=JOB_TYPE_DICT['csv_record_validation'])
        sess.add(job)
        sess.commit()

        g.user = user
        file_handler = fileHandler.FileHandler({}, is_local=True)
        response = certify_dabs_submission(submission, file_handler)
        response_json = json.loads(response.data.decode('UTF-8'))
        assert response.status_code == 400
        assert response_json['message'] == 'This submission was last validated or its D files generated before the ' \
                                           'start of the submission window ({}). Please revalidate before ' \
                                           'certifying.'.\
            format(quarter_reval.window_start.strftime('%m/%d/%Y'))


@pytest.mark.usefixtures('job_constants')
def test_certify_dabs_submission_quarterly_revalidation_multiple_thresholds(database):
    """ Tests that a DABS submission is not affected by a different quarterly revalidation threshold than the one that
        matches its reporting_start_date.
    """
    with Flask('test-app').app_context():
        now = datetime.datetime.utcnow()
        earlier = now - datetime.timedelta(days=1)
        sess = database.session

        user = UserFactory()
        cgac = CGACFactory(cgac_code='001', agency_name='CGAC Agency')
        submission = SubmissionFactory(created_at=earlier, updated_at=earlier, cgac_code=cgac.cgac_code,
                                       reporting_fiscal_period=3, reporting_fiscal_year=2017,
                                       reporting_start_date='2016-10-01', is_quarter_format=True, publishable=True,
                                       publish_status_id=PUBLISH_STATUS_DICT['unpublished'], d2_submission=False,
                                       number_of_errors=0, number_of_warnings=200, certifying_user_id=None)
        quarter_reval = QuarterlyRevalidationThresholdFactory(year=2017, quarter=1, window_start=earlier)
        quarter_reval_2 = QuarterlyRevalidationThresholdFactory(year=2017, quarter=2,
                                                                window_start=now + datetime.timedelta(days=10))
        sess.add_all([user, cgac, submission, quarter_reval, quarter_reval_2])
        sess.commit()

        job = JobFactory(submission_id=submission.submission_id, last_validated=now,
                         job_type_id=JOB_TYPE_DICT['csv_record_validation'])
        sess.add(job)
        sess.commit()

        g.user = user
        file_handler = fileHandler.FileHandler({}, is_local=True)
        response = certify_dabs_submission(submission, file_handler)
        assert response.status_code == 200


@pytest.mark.usefixtures('job_constants')
def test_certify_dabs_submission_reverting(database):
    """ Tests that a DABS submission cannot be certified while reverting. """
    with Flask('test-app').app_context():
        now = datetime.datetime.utcnow()
        earlier = now - datetime.timedelta(days=1)
        sess = database.session

        user = UserFactory()
        cgac = CGACFactory(cgac_code='001', agency_name='CGAC Agency')
        submission = SubmissionFactory(created_at=earlier, updated_at=earlier, cgac_code=cgac.cgac_code,
                                       reporting_fiscal_period=3, reporting_fiscal_year=2017,
                                       reporting_start_date='2016-10-01', is_quarter_format=True, publishable=True,
                                       publish_status_id=PUBLISH_STATUS_DICT['reverting'], d2_submission=False,
                                       number_of_errors=0, number_of_warnings=200, certifying_user_id=None)
        sess.add_all([user, cgac, submission])
        sess.commit()

        g.user = user
        file_handler = fileHandler.FileHandler({}, is_local=True)
        response = certify_dabs_submission(submission, file_handler)
        response_json = json.loads(response.data.decode('UTF-8'))
        assert response.status_code == 400
        assert response_json['message'] == 'Submission is certifying or reverting'


@pytest.mark.usefixtures('error_constants')
@pytest.mark.usefixtures('job_constants')
def test_revert_submission(database, monkeypatch):
    """ Tests reverting an updated DABS certification """
    sess = database.session

    sub = Submission(publish_status_id=PUBLISH_STATUS_DICT['updated'], is_quarter_format=True, d2_submission=False,
                     publishable=False, number_of_errors=20, number_of_warnings=15)
    sess.add(sub)
    sess.commit()

    job = Job(submission_id=sub.submission_id, job_status_id=JOB_STATUS_DICT['finished'],
              job_type_id=JOB_TYPE_DICT['csv_record_validation'], file_type_id=FILE_TYPE_DICT['appropriations'],
              number_of_warnings=0, number_of_errors=10, filename='new/test/file.csv', number_of_rows=5,
              number_of_rows_valid=0)
    cert_history = CertifyHistory(submission_id=sub.submission_id)
    sess.add_all([job, cert_history])
    sess.commit()

    cert_approp = CertifiedAppropriation(submission_id=sub.submission_id, job_id=job.job_id, row_number=1,
                                         spending_authority_from_of_cpe=2, tas='test')
    approp = Appropriation(submission_id=sub.submission_id, job_id=job.job_id, row_number=1,
                           spending_authority_from_of_cpe=15, tas='test')
    cert_files = CertifiedFilesHistory(certify_history_id=cert_history.certify_history_id,
                                       submission_id=sub.submission_id, filename='old/test/file2.csv',
                                       file_type_id=FILE_TYPE_DICT['appropriations'], warning_filename='a/warning.csv')
    cert_meta1 = CertifiedErrorMetadata(job_id=job.job_id, file_type_id=FILE_TYPE_DICT['appropriations'],
                                        target_file_type_id=None, occurrences=15)
    cert_meta2 = CertifiedErrorMetadata(job_id=job.job_id, file_type_id=FILE_TYPE_DICT['appropriations'],
                                        target_file_type_id=None, occurrences=10)
    file_entry = File(file_id=FILE_TYPE_DICT['appropriations'], job_id=job.job_id,
                      file_status_id=FILE_STATUS_DICT['incomplete'], headers_missing='something')
    sess.add_all([cert_approp, approp, cert_files, cert_meta1, cert_meta2, file_entry])
    sess.commit()

    file_handler = fileHandler.FileHandler({}, is_local=True)
    monkeypatch.setattr(file_handler, 'revert_certified_error_files', Mock())
    revert_to_certified(sub, file_handler)

    # Test that certified data is moved back
    approp_query = sess.query(Appropriation).filter_by(submission_id=sub.submission_id).all()
    assert len(approp_query) == 1
    assert approp_query[0].spending_authority_from_of_cpe == 2

    # Test that the job got updated
    job_query = sess.query(Job).filter_by(submission_id=sub.submission_id).all()
    assert len(job_query) == 1
    assert job_query[0].filename == CONFIG_BROKER['broker_files'] + 'file2.csv'
    assert job_query[0].number_of_warnings == 25
    assert job_query[0].number_of_errors == 0
    assert job_query[0].number_of_rows == 2
    assert job_query[0].number_of_rows_valid == 1

    # Test that File got updated
    file_query = sess.query(File).filter_by(job_id=job.job_id).all()
    assert len(file_query) == 1
    assert file_query[0].headers_missing is None
    assert file_query[0].file_status_id == FILE_STATUS_DICT['complete']

    # Make sure submission got updated
    sub_query = sess.query(Submission).filter_by(submission_id=sub.submission_id).all()
    assert len(sub_query) == 1
    assert sub_query[0].publishable is True
    assert sub_query[0].number_of_errors == 0
    assert sub_query[0].number_of_warnings == 25


@pytest.mark.usefixtures('job_constants')
def test_revert_submission_fabs_submission(database):
    """ Tests reverting an updated DABS certification failure for FABS submission """
    sess = database.session

    sub = Submission(d2_submission=True)
    sess.add(sub)
    sess.commit()

    file_handler = fileHandler.FileHandler({}, is_local=True)
    with pytest.raises(ResponseException) as resp_except:
        revert_to_certified(sub, file_handler)

    assert resp_except.value.status == 400
    assert str(resp_except.value) == 'Submission must be a DABS submission.'


@pytest.mark.usefixtures('job_constants')
def test_revert_submission_not_updated_submission(database):
    """ Tests reverting an updated DABS certification failure for non-updated submission """
    sess = database.session

    sub1 = Submission(publish_status_id=PUBLISH_STATUS_DICT['published'], d2_submission=False)
    sub2 = Submission(publish_status_id=PUBLISH_STATUS_DICT['unpublished'], d2_submission=False)
    sess.add_all([sub1, sub2])
    sess.commit()

    file_handler = fileHandler.FileHandler({}, is_local=True)
    # Certified submission
    with pytest.raises(ResponseException) as resp_except:
        revert_to_certified(sub1, file_handler)

    assert resp_except.value.status == 400
    assert str(resp_except.value) == 'Submission has not been certified or has not been updated since certification.'

    # Uncertified submission
    with pytest.raises(ResponseException) as resp_except:
        revert_to_certified(sub2, file_handler)

    assert resp_except.value.status == 400
    assert str(resp_except.value) == 'Submission has not been certified or has not been updated since certification.'


@pytest.mark.usefixtures('job_constants')
def test_move_certified_data(database):
    """ Tests the move_certified_data function """
    with Flask('test-app').app_context():
        sess = database.session

        # Create 2 submissions
        sub_1 = SubmissionFactory()
        sub_2 = SubmissionFactory()
        sess.add_all([sub_1, sub_2])
        sess.commit()

        # Create jobs so we can put a job ID into the tables
        job_1 = JobFactory(submission_id=sub_1.submission_id)
        job_2 = JobFactory(submission_id=sub_2.submission_id)
        sess.add_all([job_1, job_2])
        sess.commit()

        # Create Appropriation entries, 1 per submission, and one of each other kind
        approp_1 = Appropriation(submission_id=sub_1.submission_id, job_id=job_1.job_id, row_number=1,
                                 spending_authority_from_of_cpe=2)
        approp_2 = Appropriation(submission_id=sub_2.submission_id, job_id=job_2.job_id, row_number=1,
                                 spending_authority_from_of_cpe=2)
        ocpa = ObjectClassProgramActivity(submission_id=sub_1.submission_id, job_id=job_1.job_id, row_number=1)
        award_fin = AwardFinancial(submission_id=sub_1.submission_id, job_id=job_1.job_id, row_number=1)
        error_1 = ErrorMetadata(job_id=job_1.job_id)
        error_2 = ErrorMetadata(job_id=job_2.job_id)
        sess.add_all([approp_1, approp_2, ocpa, award_fin, error_1, error_2])
        sess.commit()

        move_certified_data(sess, sub_1.submission_id)

        # There are 2 entries, we only want to move the 1 with the submission ID that matches
        approp_query = sess.query(CertifiedAppropriation).filter_by(submission_id=sub_1.submission_id).all()
        assert len(approp_query) == 1
        assert approp_query[0].spending_authority_from_of_cpe == 2

        # Make sure the others got moved as well
        ocpa_query = sess.query(CertifiedObjectClassProgramActivity).filter_by(submission_id=sub_1.submission_id).all()
        award_query = sess.query(CertifiedAwardFinancial).filter_by(submission_id=sub_1.submission_id).all()
        # Query all job IDs but only one result should show up
        error_query = sess.query(CertifiedErrorMetadata).\
            filter(CertifiedErrorMetadata.job_id.in_([job_1.job_id, job_2.job_id])).all()
        assert len(ocpa_query) == 1
        assert len(award_query) == 1
        assert len(error_query) == 1

        # Change the Appropriation data
        approp_1.spending_authority_from_of_cpe = 5
        sess.refresh(approp_1)

        # Move the data again (recertify) and make sure we didn't add extras, just adjusted the one we had
        move_certified_data(sess, sub_1.submission_id)
        approp_query = sess.query(CertifiedAppropriation).filter_by(submission_id=sub_1.submission_id).all()
        assert len(approp_query) == 1
        assert approp_query[0].spending_authority_from_of_cpe == 2
