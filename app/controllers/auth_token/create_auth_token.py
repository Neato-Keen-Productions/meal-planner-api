from flask import g, Blueprint
import datetime

from app.constants import USERNAME_KEY, PASSWORD_KEY
from app.controllers import get_required_key_from_params
from app.controllers.auth_token.require_auth import auth_required
from app.dao.user_dao import get_user_from_username
from app.models.auth_token import AuthToken
from app.models.http_error import HTTPError

auth_blueprint = Blueprint('mod_auth', __name__)


@auth_blueprint.route('', methods=['POST'])
def create_token_route():
    supplied_username = get_required_key_from_params(USERNAME_KEY, g.request_params)
    supplied_password = get_required_key_from_params(PASSWORD_KEY, g.request_params)

    if supplied_username is not None and supplied_password is not None:
        user = get_user_from_username(supplied_username)

        if user is not None and user.check_hashed_password(supplied_password):
            create_token_for_user(user)
        else:
            HTTPError.add_http_error_to(g.response, HTTPError.auth_invalid())

    return g.response


@auth_blueprint.route('/refresh', methods=['GET'])
@auth_required
def refresh_token():
    create_token_for_user(g.user)
    return g.response


def create_token_for_user(user):
    duration = datetime.timedelta(days=30)
    auth_token = AuthToken(user.uuid, duration)
    validity_time = datetime.datetime.now() + duration
    # TODO: Enable secure when using HTTPS on non-dev machine
    g.response.set_cookie("auth_token",
                          auth_token.encoded_value,
                          expires=validity_time,
                          domain="127.0.0.1",
                          httponly=True,
                          secure=False)
    g.response.response = {"data": {"auth_token": auth_token.encoded_value}}



