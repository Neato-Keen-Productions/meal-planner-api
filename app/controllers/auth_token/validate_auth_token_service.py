from app.dao.user_dao import get_user_from_uuid
from app.controllers.auth_token import AuthTokenStatus
from app.models.http_error import HTTPError
from app.models.user import User


def valid_user_from_auth_token(auth_token):
    error = handle_decoding_errors(auth_token)
    if error:
        return None, error

    user, error = get_user_from_uuid_handling_error(auth_token.subject)
    if error:
        return user, error

    if user.is_blacklisted:
        error = HTTPError.forbidden()
        user = None

    return user, error


def handle_decoding_errors(auth_token):
    error = None

    if auth_token.status is AuthTokenStatus.EXPIRED:
        error = HTTPError.auth_expired()
    elif auth_token.status is AuthTokenStatus.INVALID:
        error = HTTPError.auth_invalid()

    return error


def get_user_from_uuid_handling_error(uuid):
    user = get_user_from_uuid(uuid)
    error = None

    if user is None:
        error = HTTPError.not_found(User.__name__)

    return user, error




