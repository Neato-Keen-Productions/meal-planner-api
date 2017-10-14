from tests.functional import FunctionalTestCase
from tests.mocks.ingredient_mock import TEST_INGREDIENT_NAME, mock_ingredient
import json
from app.dao.ingredient_dao import get_ingredient_from_name
from tests.functional.constants import HTTP_CODE_201_CREATED, HTTP_CODE_409_CONFLICT, HTTP_CODE_422_UNPROCESSABLE_ENTITY

INGREDIENT_KEY = "ingredient"
MIN_INGREDIENT_NAME_LENGTH = 2
MAx_INGREDIENT_NAME_LENGTH = 255
LONG_INGREDIENT_NAME = "LoremipsumdolorsitametconsecteturadipiscingelitPhasellusfeugiataliqueturnaeuconvallisNuncutpurussollicitudinmollisnibhnoninterdummagnaDonecvestibulumrhoncusnullasedlaoreetmassafeugiatvelNullamloremvelitdignissimsedsemneclobortisauctornisiNullahendreritsemno"


class CreateIngredientTestCase(FunctionalTestCase):
    """This class is used to test all inputs and outputs of the POST /ingredient endpoint"""

    def test_create_ingredient_success(self):
        request_params = {INGREDIENT_KEY: TEST_INGREDIENT_NAME}
        response = self.client.post('/ingredient', data=json.dumps(request_params))
        ingredient = get_ingredient_from_name(TEST_INGREDIENT_NAME)
        self.assertIsNotNone(ingredient, "created ingredient not found")
        self.check_response_code(response, HTTP_CODE_201_CREATED)

    def test_create_ingredient_name_too_short_failure(self):
        request_params = {INGREDIENT_KEY: "1"}
        self.make_and_check_Ingredient_attempt_with_error(request_params, 801)

    def test_create_ingredient_name_too_long_failure(self):
        request_params = {INGREDIENT_KEY: LONG_INGREDIENT_NAME}
        self.make_and_check_Ingredient_attempt_with_error(request_params, 802)

    def make_and_check_Ingredient_attempt_with_error(self, request_params, app_error_code):
        response = self.client.post('/ingredient', data=json.dumps(request_params))
        ingredient = get_ingredient_from_name(request_params[INGREDIENT_KEY])
        self.assertIsNone(ingredient)
        self.check_response_code_and_headers(response, HTTP_CODE_422_UNPROCESSABLE_ENTITY)
        self.check_response_contains_only_error(app_error_code, response)

    # Conflict Check
    def test_create_ingredient_name_taken_failure(self):
        ingredient = mock_ingredient()
        self.save_objects(ingredient)
        request_params = {INGREDIENT_KEY:TEST_INGREDIENT_NAME}
        response = self.client.post('/ingredient', data=json.dumps(request_params))
        self.check_response_code_and_headers(response, HTTP_CODE_409_CONFLICT)
        self.check_response_contains_only_error(800, response)
