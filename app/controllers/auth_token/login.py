from flask import Blueprint, g
import datetime
from app.constants import USERNAME_KEY, PASSWORD_KEY
from app.controllers import get_required_key_from_params
from app.dao.user_dao import get_user_from_username
from app.models import db
from app.models.authorization import Authorization
from app.models.error import Error

auth_blueprint = Blueprint('mod_auth', __name__)


@auth_blueprint.route('/token',  methods=['POST'])
def login():
    supplied_username = get_required_key_from_params(USERNAME_KEY, g.request_params)
    supplied_password = get_required_key_from_params(PASSWORD_KEY, g.request_params)

    if supplied_username is not None and supplied_password is not None:
        user = get_user_from_username(supplied_username)

        if user is not None and user.check_hashed_password(supplied_password):
            auth = Authorization(user)
            db.session.add(auth)
            db.session.commit()
            time = datetime.datetime.now() + datetime.timedelta(days=30)
            g.response.set_cookie("auth_token", auth.token, expires=time, domain="127.0.0.1")
            g.response.response = {"data": {"auth_token": auth.token}}
        else:
            Error.add_to(g.response.response, Error.auth_invalid())

    return g.response


