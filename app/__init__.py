
from flask import Flask, g, request

# DB Models
from app.models import db
from app.models.user import User
from app.models.authorization import Authorization

# Blueprints
from app.controllers.auth.login import auth_blueprint
from app.controllers.user.create_user import user_blueprint
from app.controllers.ingredient.create_ingredient import ingredient_blueprint


def create_app():
    # Define the WSGI application object and configurations
    app = Flask(__name__)
    app.config.from_object('config.config')

    # Define the database object which is imported by modules and controllers
    # (See http://stackoverflow.com/a/9695045/604003 for explanation)
    db.init_app(app)
    db.app = app
    db.create_all()

    return app

# Create an app and its endpoints
app = create_app()
app.register_blueprint(auth_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(ingredient_blueprint)


# Initialize response objects for controller requests
@app.before_request
def before_request():
    # Initialize a response
    g.response = {}
    g.request_params = request.get_json(force=True)
