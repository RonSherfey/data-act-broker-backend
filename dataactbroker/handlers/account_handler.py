import logging
from operator import attrgetter
import requests
import xmltodict

from flask import g

from dataactbroker.handlers.aws.sesEmail import SesEmail
from dataactbroker.handlers.aws.session import LoginSession
from dataactcore.utils.jsonResponse import JsonResponse
from dataactcore.utils.requestDictionary import RequestDictionary
from dataactcore.interfaces.db import GlobalDB
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy import func, or_

from dataactcore.models.userModel import User, UserAffiliation
from dataactcore.models.domainModels import CGAC, FREC
from dataactcore.models.jobModels import Submission
from dataactcore.utils.statusCode import StatusCode
from dataactcore.interfaces.function_bag import get_email_template, check_correct_password
from dataactcore.config import CONFIG_BROKER
from dataactcore.models.lookups import PERMISSION_SHORT_DICT, DABS_PERMISSION_ID_LIST, FABS_PERMISSION_ID_LIST


logger = logging.getLogger(__name__)


class AccountHandler:
    """ This class contains the login / logout  functions

        Attributes:
            is_local: A boolean indicating if the application is being run locally or not
            request: A Flask object containing the data from the request
            bcrypt: A Bcrypt object associated with the app

        Constants:
            FRONT_END: A string indicating the URL of the front end of the app
    """
    # Handles login process, compares username and password provided
    FRONT_END = ""
    # Instance fields include request, response, logFlag, and logFile

    def __init__(self, request, bcrypt=None, is_local=False):
        """ Creates the Login Handler

            Args:
                request: Flask request object
                bcrypt: Bcrypt object associated with app
        """
        self.is_local = is_local
        self.request = request
        self.bcrypt = bcrypt

    def login(self, session):
        """ Logs a user in if their password matches using local data

            Args:
                session: the Session object from flask

            Returns:
                A JsonResponse containing the user information or details on which error occurred, such as whether a
                type was wrong, something wasn't implemented, invalid keys were provided, login was denied, or a
                different, unexpected error occurred.
        """
        try:
            sess = GlobalDB.db().session
            safe_dictionary = RequestDictionary(self.request)

            username = safe_dictionary.get_value('username')
            password = safe_dictionary.get_value('password')

            try:
                user = sess.query(User).filter(func.lower(User.email) == func.lower(username)).one()
            except Exception:
                raise ValueError("Invalid username and/or password")

            try:
                if check_correct_password(user, password, self.bcrypt):
                    # We have a valid login
                    return self.create_session_and_response(session, user)
                else:
                    raise ValueError("Invalid username and/or password")
            except ValueError as ve:
                LoginSession.logout(session)
                raise ve
            except Exception as e:
                LoginSession.logout(session)
                raise e

        # Catch any specifically raised errors or any other errors that may have happened and return them cleanly
        except (TypeError, KeyError, NotImplementedError) as e:
            # Return a 400 with appropriate message
            return JsonResponse.error(e, StatusCode.CLIENT_ERROR)
        except ValueError as e:
            # Return a 401 for login denied
            return JsonResponse.error(e, StatusCode.LOGIN_REQUIRED)
        except Exception as e:
            # Return 500
            return JsonResponse.error(e, StatusCode.INTERNAL_ERROR)

    def max_login(self, session):
        """ Logs a user in if their password matches using MAX

            Args:
                session: Session object from flask

            Returns:
                A JsonResponse containing the user information or details on which error occurred, such as whether a
                type was wrong, something wasn't implemented, invalid keys were provided, login was denied, or a
                different, unexpected error occurred.
        """
        try:
            safe_dictionary = RequestDictionary(self.request)

            ticket = safe_dictionary.get_value("ticket")
            service = safe_dictionary.get_value('service')

            # Call MAX's serviceValidate endpoint and retrieve the response
            max_dict = get_max_dict(ticket, service)

            if 'cas:authenticationSuccess' not in max_dict['cas:serviceResponse']:
                raise ValueError("The Max CAS endpoint was unable to locate your session "
                                 "using the ticket/service combination you provided.")
            cas_attrs = max_dict['cas:serviceResponse']['cas:authenticationSuccess']['cas:attributes']

            # Grab MAX ID to see if a service account is being logged in
            max_id_components = cas_attrs['maxAttribute:MAX-ID'].split('_')
            service_account_flag = (len(max_id_components) > 1 and max_id_components[0].lower() == 's')

            # Grab the email and list of groups from MAX's response
            email = cas_attrs['maxAttribute:Email-Address']

            try:
                sess = GlobalDB.db().session
                user = sess.query(User).filter(func.lower(User.email) == func.lower(email)).one_or_none()

                # If the user does not exist, create them since they are allowed to access the site because they got
                # past the above group membership checks
                if user is None:
                    user = User()
                    user.email = email

                set_user_name(user, cas_attrs)

                set_max_perms(user, cas_attrs['maxAttribute:GroupList'], service_account_flag)

                sess.add(user)
                sess.commit()

            except MultipleResultsFound:
                raise ValueError("An error occurred during login.")

            return self.create_session_and_response(session, user)

        # Catch any specifically raised errors or any other errors that may have happened and return them cleanly.
        # We add the error parameter here because this endpoint needs to provide better feedback, and to avoid changing
        # the default behavior of the JsonResponse class globally.
        except (TypeError, KeyError, NotImplementedError) as e:
            # Return a 400 with appropriate message
            return JsonResponse.error(e, StatusCode.CLIENT_ERROR, error=str(e))
        except ValueError as e:
            # Return a 401 for login denied
            return JsonResponse.error(e, StatusCode.LOGIN_REQUIRED, error=str(e))
        except Exception as e:
            # Return 500
            return JsonResponse.error(e, StatusCode.INTERNAL_ERROR, error=str(e))

    @staticmethod
    def create_session_and_response(session, user):
        """ Create a session.

            Args:
                session: Session object from flask
                user: Users object

            Returns:
                JsonResponse containing the JSON for the user
        """
        LoginSession.login(session, user.user_id)
        data = json_for_user(user, session['sid'])
        data['message'] = 'Login successful'
        return JsonResponse.create(StatusCode.OK, data)

    @staticmethod
    def set_skip_guide(skip_guide):
        """ Set current user's skip guide parameter

            Args:
                skip_guide: boolean indicating whether the skip guide should be visible or not for this user

            Returns:
                JsonResponse object containing results of setting the skip guide or details of the error that occurred.
                Possible errors include the request not containing a skip_guide parameter or it not being a boolean
                value
        """
        sess = GlobalDB.db().session
        g.user.skip_guide = skip_guide
        sess.commit()
        return JsonResponse.create(StatusCode.OK, {'message': 'skip_guide set successfully', 'skip_guide': skip_guide})

    @staticmethod
    def email_users(submission, system_email, template_type, user_ids):
        """ Send email notification to list of users

            Args:
                submission: the submission to send the email about
                system_email: the address of the system to send the email from
                template_type: the template type of the email to send
                user_ids: A list of user IDs denoting who to send the email to

            Returns:
                A JsonReponse containing a message that the email sent successfully or the details of the missing
                or incorrect parameters
        """
        sess = GlobalDB.db().session

        if submission.cgac_code:
            agency = sess.query(CGAC).filter_by(cgac_code=submission.cgac_code).first()
        else:
            agency = sess.query(FREC).filter_by(frec_code=submission.frec_code).first()

        if not agency:
            return JsonResponse.error(ValueError("The requested submission is not aligned to a valid CGAC or FREC "
                                                 "agency"), StatusCode.CLIENT_ERROR)

        # Check if email template type is valid
        get_email_template(template_type)

        link = "".join([AccountHandler.FRONT_END, '#/submission/', str(submission.submission_id)])
        email_template = {'[REV_USER_NAME]': g.user.name, '[REV_AGENCY]': agency.agency_name, '[REV_URL]': link}

        users = []
        for user_id in user_ids:
            # Check if user id is valid, if so add User object to array
            users.append(sess.query(User).filter(User.user_id == user_id).one())

        for user in users:
            new_email = SesEmail(user.email, system_email, template_type=template_type, parameters=email_template)
            new_email.send()

        return JsonResponse.create(StatusCode.OK, {"message": "Emails successfully sent"})


def perms_to_affiliations(perms, user_id, service_account_flag=False):
    """ Convert a list of perms from MAX to a list of UserAffiliations. Filter out and log any malformed perms

        Args:
            perms: list of permissions (as strings) for the user
            user_id: the ID of the user
            service_account_flag: flag to indicate a service account
        Yields:
            UserAffiliations based on the permissions provided
    """
    available_cgacs = {cgac.cgac_code: cgac for cgac in GlobalDB.db().session.query(CGAC)}
    available_frecs = {frec.frec_code: frec for frec in GlobalDB.db().session.query(FREC)}
    log_data = {
        'message_type': 'BrokerWarning',
        'user_id': user_id
    }
    for perm in perms:
        log_data['message'] = 'User with ID {} has malformed permission: {}'.format(user_id, perm)
        components = perm.split('-PERM_')
        if len(components) != 2:
            logger.warning(log_data)
            continue

        codes, perm_level = components
        split_codes = codes.split('-FREC_')
        frec_code, cgac_code = None, None
        if len(split_codes) == 2:
            # permissions for FR entity code and readonly CGAC
            frec_code, cgac_code = split_codes[1], split_codes[0]
            if frec_code not in available_frecs or cgac_code not in available_cgacs:
                logger.warning(log_data)
                continue
        else:
            # permissions for CGAC
            cgac_code = codes
            if cgac_code not in available_cgacs:
                logger.warning(log_data)
                continue

        perm_level = perm_level.lower()

        if service_account_flag:
            # Replace MAX Service Account permissions with Broker "write" and "editfabs" permissions
            perm_level = 'we'
        elif perm_level not in 'rwsef':
            logger.warning(log_data)
            continue

        for permission in perm_level:
            if frec_code:
                yield UserAffiliation(
                    cgac=available_cgacs[cgac_code],
                    frec=None,
                    permission_type_id=PERMISSION_SHORT_DICT['r']
                )
                yield UserAffiliation(
                    cgac=None,
                    frec=available_frecs[frec_code],
                    permission_type_id=PERMISSION_SHORT_DICT[permission]
                )
            else:
                yield UserAffiliation(
                    cgac=available_cgacs[cgac_code] if cgac_code else None,
                    frec=None,
                    permission_type_id=PERMISSION_SHORT_DICT[permission]
                )


def best_affiliation(affiliations):
    """ If a user has multiple permissions for a single agency, select the best

        Args:
            affiliations: list of UserAffiliations a user has

        Returns:
            List of all affiliations the user has (with duplicates, highest of each type/agency provided)
    """
    dabs_dict, fabs_dict = {}, {}

    # Sort all affiliations from lowest to highest permission
    sorted_affiliations = sorted(list(affiliations), key=attrgetter('permission_type_id'))

    for affiliation in sorted_affiliations:
        # Overwrite low permissions with high permissions; keep DABS and FABS separate so FABS doesn't overwrite DABS
        if affiliation.permission_type_id in DABS_PERMISSION_ID_LIST:
            dabs_dict[affiliation.cgac, affiliation.frec] = affiliation
        elif affiliation.permission_type_id in FABS_PERMISSION_ID_LIST:
            fabs_dict[affiliation.cgac, affiliation.frec] = affiliation

    all_affils = list(dabs_dict.values()) + list(fabs_dict.values())
    return all_affils


def set_user_name(user, cas_attrs):
    """ Update the name for the user based on the MAX attributes.

        Args:
            user: the User object
            cas_attrs: a dictionary of the max attributes (includes first, middle, last names) for a logged in user
    """
    first_name = cas_attrs['maxAttribute:First-Name']
    middle_name = cas_attrs['maxAttribute:Middle-Name']
    last_name = cas_attrs['maxAttribute:Last-Name']

    # Check for None first so the condition can short-circuit without
    # having to worry about calling strip() on a None object
    if middle_name is None or middle_name.strip() == '':
        user.name = first_name + " " + last_name
    else:
        user.name = first_name + " " + middle_name[0] + ". " + last_name


def set_max_perms(user, max_group_list, service_account_flag=False):
    """ Convert the user group lists present on MAX into a list of UserAffiliations and/or website_admin status.

        Permissions are encoded as a comma-separated list of:
        {parent-group}-CGAC_{cgac-code}-PERM_{one-of-R-W-S-F}
        {parent-group}-CGAC_{cgac-code}-FREC_{frec_code}-PERM_{one-of-R-W-S-F}
        or
        {parent-group}-CGAC_SYS to indicate website_admin

        Args:
            user: the User object
            max_group_list: list of all MAX groups the user has
            service_account_flag: flag to indicate a service account
    """
    prefix = CONFIG_BROKER['parent_group'] + '-CGAC_'

    # Each group name that we care about begins with the prefix, but once we have that list, we don't need the
    # prefix anymore, so trim it off.
    if max_group_list is not None:
        perms = [group_name[len(prefix):]
                 for group_name in max_group_list.split(',')
                 if group_name.startswith(prefix)]
    elif service_account_flag:
        raise ValueError("There are no DATA Act Broker permissions assigned to this Service Account. You may request "
                         "permissions at https://community.max.gov/x/fJwuRQ")
    else:
        perms = []

    if 'SYS' in perms:
        user.affiliations = []
        user.website_admin = True
    else:
        affiliations = best_affiliation(perms_to_affiliations(perms, user.user_id, service_account_flag))

        user.affiliations = affiliations
        user.website_admin = False


def json_for_user(user, session_id):
    """ Convert the provided user to a dictionary (for JSON)

        Args:
            user: the User object

        Returns:
            An object containing user details
    """
    return {
        "user_id": user.user_id,
        "name": user.name,
        "title": user.title,
        "skip_guide": user.skip_guide,
        "website_admin": user.website_admin,
        "affiliations": [{"agency_name": affil.cgac.agency_name, "permission": affil.permission_type_name}
                         if affil.cgac else
                         {"agency_name": affil.frec.agency_name, "permission": affil.permission_type_name}
                         for affil in user.affiliations],
        "session_id": session_id
    }


def get_max_dict(ticket, service):
    """ Get the result from MAX's serviceValidate functionality

        Args:
            ticket: the ticket to send to MAX
            service: the service to send to MAX

        Returns:
            A dictionary of the response from MAX
    """
    url = CONFIG_BROKER['cas_service_url'].format(ticket, service)
    max_xml = requests.get(url).content
    return xmltodict.parse(max_xml)


def logout(session):
    """ This function removes the session from the session table if currently logged in, and then returns a success
        message

        Args:
            session: the Session object

        Returns:
            a JsonResponse that the logout was successful
    """
    # Call session handler
    LoginSession.logout(session)
    return JsonResponse.create(StatusCode.OK, {"message": "Logout successful"})


def list_user_emails():
    """ List user names and emails

        Returns:
            A JsonResponse that contains a list of user information (ID, name, and email)
    """
    sess = GlobalDB.db().session
    users = sess.query(User)
    if not g.user.website_admin:
        relevant_cgacs = [aff.cgac_id for aff in g.user.affiliations]
        subquery = sess.query(UserAffiliation.user_id).filter(UserAffiliation.cgac_id.in_(relevant_cgacs))
        users = users.filter(User.user_id.in_(subquery))

    user_info = [{"id": user.user_id, "name": user.name, "email": user.email} for user in users]
    return JsonResponse.create(StatusCode.OK, {"users": user_info})


def list_submission_users(d2_submission):
    """ List user IDs and names that have submissions that the requesting user can see.

        Arguments:
            d2_submission: boolean indicating whether it is a DABS or FABS submission (True if FABS)

        Returns:
            A JsonResponse containing a list of users that have submissions that the requesting user can see
    """

    sess = GlobalDB.db().session
    # subquery to create the EXISTS portion of the query
    exists_query = sess.query(Submission).filter(Submission.user_id == User.user_id,
                                                 Submission.d2_submission.is_(d2_submission))

    # if user is not an admin, we have to adjust the exists query to limit submissions
    if not g.user.website_admin:
        # split affiliations into frec and cgac
        cgac_affiliations = [aff for aff in g.user.affiliations if aff.cgac]
        frec_affiliations = [aff for aff in g.user.affiliations if aff.frec]

        # Don't list FABS permissions users if the user only has DABS permissions
        if not d2_submission:
            cgac_affiliations = [aff for aff in cgac_affiliations if aff.permission_type_id in DABS_PERMISSION_ID_LIST]
            frec_affiliations = [aff for aff in frec_affiliations if aff.permission_type_id in DABS_PERMISSION_ID_LIST]

        # Make a list of cgac and frec codes
        cgac_list = [aff.cgac.cgac_code for aff in cgac_affiliations]
        frec_list = [aff.frec.frec_code for aff in frec_affiliations]

        # Add filters where applicable
        affiliation_filters = [Submission.user_id == g.user.user_id]
        if cgac_list:
            affiliation_filters.append(Submission.cgac_code.in_(cgac_list))
        if frec_list:
            affiliation_filters.append(Submission.frec_code.in_(frec_list))

        exists_query = exists_query.filter(or_(*affiliation_filters))

    # Add an exists onto the query, couldn't do this earlier because then the filters couldn't get added in the if
    exists_query = exists_query.exists()

    # Get all the relevant users
    user_results = sess.query(User.user_id, User.name, User.email).filter(exists_query).order_by(User.name).all()

    # Create an array containing relevant users in a readable format
    user_list = []
    for user in user_results:
        user_list.append({'user_id': user[0], 'name': user[1], 'email': user[2]})

    return JsonResponse.create(StatusCode.OK, {"users": user_list})
