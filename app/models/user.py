from app.models import db, BaseModel


class User (BaseModel):

    __tablename__ = 'User'

    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password
