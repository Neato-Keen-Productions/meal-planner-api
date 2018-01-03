from app.models.ingredient import Ingredient

def get_ingredient_from_name(name):
    return Ingredient.query.filter_by(name=name).first()