from flask import Blueprint, g, jsonify

auth_blueprint = Blueprint('mod_auth', __name__)


@auth_blueprint.route('/login',  methods=['GET'])
def login():

    # Add the User to the return
    g.response = {"response" :"GET /login success"}

    # Return a friendly JSON greeting.
    return jsonify(**g.response)

