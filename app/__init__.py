
from flask import Flask, g, request
from flask_cors import CORS

# DB Models
from app.models import db
from app.models.user import User
from app.models.authorization import Authorization

# Blueprints
from app.controllers.auth.login import auth_blueprint
from app.controllers.user.create_user import user_blueprint


def create_app(config):
    # Define the WSGI application object and configurations
    new_app = Flask(__name__)
    new_app.config.from_object(config)
    CORS(new_app)

    # Define the database object which is imported by modules and controllers
    # (See http://stackoverflow.com/a/9695045/604003 for explanation)
    db.init_app(new_app)
    db.app = new_app
    db.create_all()

    return new_app

# Create an app and its endpoints
app = create_app('config.config')

app.register_blueprint(auth_blueprint)
app.register_blueprint(user_blueprint)


# Initialize response objects for controller requests
@app.before_request
def before_request():
    # Initialize a response
    g.response = {}

    # Get request params
    if request.method == "GET":
        g.request_params = request.args
    elif request.method in ["POST", "PUT"]:
        g.request_params = request.get_json(force=True)
    else:
        g.request_params = {}
