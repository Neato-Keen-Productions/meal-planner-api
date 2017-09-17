
from flask import Flask
from app.models import db
from app.controllers.auth.login import auth_blueprint


# Define the WSGI application object and configurations
app = Flask(__name__)
# app.config.from_object('app.config')

# Define the database object which is imported by modules and controllers
# (See http://stackoverflow.com/a/9695045/604003 for explanation)
db.init_app(app)

app.register_blueprint(auth_blueprint)