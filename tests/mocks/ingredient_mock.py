from app.models.ingredient import Ingredient

TEST_INGREDIENT_NAME = "test_ingredient"

def mock_ingredient():
    """Ingredient that contains a TEST_INGREDIENT_NAME"""
    return Ingredient(TEST_INGREDIENT_NAME)
