from flask import Blueprint, g
from app.constants import USERNAME_KEY, PASSWORD_KEY
from app.controllers import get_required_key_from_params
from app.dao.user_dao import get_user_from_username
from app.models.http_error import HTTPError
from app.models.auth_token import AuthToken
import datetime

auth_blueprint = Blueprint('mod_auth', __name__)


@auth_blueprint.route('/auth_token',  methods=['POST'])
def create_token():
    supplied_username = get_required_key_from_params(USERNAME_KEY, g.request_params)
    supplied_password = get_required_key_from_params(PASSWORD_KEY, g.request_params)

    if supplied_username is not None and supplied_password is not None:
        user = get_user_from_username(supplied_username)

        if user is not None and user.check_hashed_password(supplied_password):
            auth_token = AuthToken(user.uuid, datetime.timedelta(days=5))
            time = datetime.datetime.now() + datetime.timedelta(days=30)
            #TODO: Enable secure when using HTTPS on non-dev machine
            g.response.set_cookie("auth_token", auth_token.encoded_value, expires=time, domain="127.0.0.1", httponly=True, secure=False)
            g.response.response = {"data": {"auth_token": auth_token.encoded_value}}
        else:
            HTTPError.add_http_error_to(g.response, HTTPError.auth_invalid())

    return g.response
