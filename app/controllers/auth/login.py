from flask import request, Blueprint, g, jsonify
from app.dao.user_dao import UserDAO
from app.models.authorization import Authorization
from app.models.user import User
from app.models import db
import logging

auth_blueprint = Blueprint('mod_auth', __name__)


@auth_blueprint.route('/login',  methods=['POST'])
def login():
    g.request_params = request.get_json(force=True)
    supplied_username = g.request_params["username"]
    supplied_password = g.request_params["password"]

    user = UserDAO.get_user_from_username(supplied_username)

    if user is not None and user.check_hashed_password(supplied_password):
        auth = Authorization(user)
        db.session.add(auth)
        db.session.commit()
        g.response = {"data": {"auth_token": auth.token}}
    else:
        g.response = {"errors": [{"code": 00000, "message": "Auth Failed"}]}

    return jsonify(**g.response)

