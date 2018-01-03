from flask import Blueprint, g, jsonify, Response
from app.controllers import get_required_key_from_params
from app.constants import INGREDIENT_KEY, MIN_INGREDIENT_NAME_LENGTH, MAX_INGREDIENT_NAME_LENGTH, ERRORS_KEY
from app.models.error import Error
from app.dao.ingredient_dao import get_ingredient_from_name
from app.models import db
from app.models.ingredient import Ingredient

ingredient_blueprint = Blueprint('mod_ingredient', __name__)


@ingredient_blueprint.route('/ingredient', methods=['POST'])
def create():
    supplied_ingredient = get_required_key_from_params(INGREDIENT_KEY, g.request_params)

    # check ingredient name is not too short
    if len(supplied_ingredient) < MIN_INGREDIENT_NAME_LENGTH:
        Error.add_to(g.response, Error.ingredient_name_too_short())
    # check ingredient name is not too long
    if len(supplied_ingredient) > MAX_INGREDIENT_NAME_LENGTH:
        Error.add_to(g.response, Error.ingredient_name_too_long())

    if ERRORS_KEY in g.response:
        return jsonify(**g.response), 422
    # check ingredient name is not already taken
    if get_ingredient_from_name(supplied_ingredient) is not None:
        Error.add_to(g.response, Error.ingredient_name_taken())
        return jsonify(**g.response), 409

    ingredient = Ingredient(supplied_ingredient)
    db.session.add(ingredient)
    db.session.commit()
    return Response(status=201, mimetype='application/json')
