import hashlib
import random
import uuid

from app.models import db, BaseModel


class User (BaseModel):

    __tablename__ = 'User'

    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(255))
    is_blacklisted = db.Column(db.Boolean, default=False)

    def __init__(self, username, password):
        super(User, self).__init__()
        self.username = username
        self.salt = '%020x' % random.randrange(16**30)
        self.password = self.__hash_password__(password)

    def __hash_password__(self, password_to_hash):
        m = hashlib.sha256()
        m.update(self.salt + password_to_hash)
        return m.hexdigest()

    def check_hashed_password(self, supplied_password):
        return self.password == self.__hash_password__(supplied_password)
