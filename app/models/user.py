import hashlib
import random

from app.models import db, BaseModel

# Imports required for one-to-many inverse relations
from app.models.authorization import Authorization


class User (BaseModel):

    __tablename__ = 'User'

    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(255))
    authorizations = db.relationship(Authorization.__tablename__, back_populates="user")

    def __init__(self, username, password):
        self.username = username
        self.salt = '%020x' % random.randrange(16**30)
        self.password = self.__hash_password__(password)

    def __hash_password__(self, password_to_hash):
        m = hashlib.sha256()
        m.update(self.salt + password_to_hash)
        return m.hexdigest()

    def check_hashed_password(self, supplied_password):
        return self.password == self.__hash_password__(supplied_password)
