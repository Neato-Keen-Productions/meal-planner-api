from app.models import db, BaseModel
import random


class Authorization (BaseModel):

    __tablename__ = 'Authorization'

    token = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))
    user = db.relationship("User", primaryjoin="Authorization.user_id==User.id")

    def __init__(self, user):
        self.token = '%08x' % random.randrange(16 ** 30)
        self.user = user
