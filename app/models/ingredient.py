from app.models import db, BaseModel


class Ingredient (BaseModel):
    __tablename__ = 'Ingredient'

    name = db.Column(db.String(255), nullable=False)

    def __init__(self, name):
        self.name = name

