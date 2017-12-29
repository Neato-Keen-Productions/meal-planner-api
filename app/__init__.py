
from flask import Flask, g, request, make_response, url_for
from flask_cors import CORS
import json
from app.models.auth_token import AuthToken
from app.controllers.auth_token.validate_auth_token_service import valid_user_from_auth_token
from app.models.error import Error

# DB Models
from app.models import db
from app.models.user import User

# Blueprints
from app.controllers.auth_token.create_auth_token import auth_blueprint
from app.controllers.user.create_user import user_blueprint


def create_app(config):
    # Define the WSGI application object and configurations
    new_app = Flask(__name__)
    new_app.config.from_object(config)
    CORS(new_app, allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials"], supports_credentials=True)
    return new_app


def init_db(new_app):
    # Define the database object which is imported by modules and controllers
    # (See http://stackoverflow.com/a/9695045/604003 for explanation)
    db.init_app(new_app)
    db.app = new_app
    db.create_all()


def register_blueprints(new_app):
    new_app.register_blueprint(auth_blueprint, url_prefix='/auth_token')
    new_app.register_blueprint(user_blueprint, url_prefix='/user')


# Create an app and its endpoints
app = create_app('config.config')
init_db(app)
register_blueprints(app)


@app.before_request
def before_request():
    prepare_response()
    set_user_from_cookies(request.cookies)
    prepare_request_params()


def prepare_response():
    g.response = make_response()
    g.response.response = {}
    g.response.headers['content-type'] = 'application/json'


def set_user_from_cookies(cookies):
    if "auth_token" in cookies:
        find_user_from_encoded_token(cookies["auth_token"])
    else:
        g.user = None


def find_user_from_encoded_token(encoded_auth_token_value):
    auth_token = AuthToken(encoded_value=encoded_auth_token_value)
    g.user, error = valid_user_from_auth_token(auth_token)
    if error:
        Error.add_to_response_dict(g.response.response, error)


def prepare_request_params():
    if request.method == "GET":
        g.request_params = request.args
    elif request.method in ["POST", "PUT"]:
        g.request_params = request.get_json(force=True)
    else:
        g.request_params = {}


@app.after_request
def after_request(response):
    if response.response is not None and type(response.response) is dict:
        response.data = json.dumps(response.response)
    return response


