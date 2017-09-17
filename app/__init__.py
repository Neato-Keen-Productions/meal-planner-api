
from flask import Flask
from app.auth.login import auth_blueprint


# Define the WSGI application object and configurations
app = Flask(__name__)
# app.config.from_object('app.config')

app.register_blueprint(auth_blueprint)