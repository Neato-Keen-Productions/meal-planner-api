
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# Define a base model for other database tables to inherit
class BaseModel(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    time_created = db.Column(db.DateTime, default=db.func.current_timestamp())
