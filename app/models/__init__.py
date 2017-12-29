from flask_sqlalchemy import SQLAlchemy
import uuid

db = SQLAlchemy()


# Define a base model for other database tables to inherit
class BaseModel(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(36), unique=True)
    time_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self):
        self.uuid = str(uuid.uuid4())
