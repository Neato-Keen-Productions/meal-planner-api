from flask import request, Blueprint, g, jsonify
import logging

auth_blueprint = Blueprint('mod_auth', __name__)


@auth_blueprint.route('/login',  methods=['POST'])
def login():
    g.request_params = request.get_json(force=True)
    username = g.request_params["username"]
    password = g.request_params["password"]
    logging.debug(username)
    logging.debug(password)

    # Add the User to the return
    g.response = {"response": "GET /login success"}

    # Return a friendly JSON greeting.
    return jsonify(**g.response)

