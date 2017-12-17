
from flask import Flask, g, request, make_response
from flask_cors import CORS
import json

# DB Models
from app.models import db
from app.models.user import User
from app.models.authorization import Authorization

# Blueprints
from app.controllers.auth_token.login import auth_blueprint
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
    new_app.register_blueprint(auth_blueprint)
    new_app.register_blueprint(user_blueprint)

# Create an app and its endpoints
app = create_app('config.config')
init_db(app)
register_blueprints(app)


# Initialize response objects for controller requests
@app.before_request
def before_request():
    # Initialize a response
    g.response = make_response()
    g.response.response = {}
    g.response.headers['content-type'] = 'application/json'

    # Get request params
    if request.method == "GET":
        g.request_params = request.args
    elif request.method in ["POST", "PUT"]:
        g.request_params = request.get_json(force=True)
    else:
        g.request_params = {}

@app.after_request
def after_request(response):
    if response.response is not None:
        response.data = json.dumps(response.response)
    return response
