import json
from tests.functional import FunctionalTestCase
from tests.mocks.user_mock import TEST_PASSWORD, TEST_USERNAME, mock_user
from tests.functional.constant_keys import USERNAME_KEY, PASSWORD_KEY
from app.dao.user_dao import get_user_from_username
from app.models.user import User
from tests.functional.constants import *



MAX_PASSWORD_LENGTH = 256
MIN_PASSWORD_LENGTH = 6
MAX_USERNAME_LEGNTH = 32
MIN_USERNAME_LENGTH = 3
LONG_PASSWORD = "LoremipsumdolorsitametconsecteturadipiscingelitPhasellusfeugiataliqueturnaeuconvallisNuncutpurussollicitudinmollisnibhnoninterdummagnaDonecvestibulumrhoncusnullasedlaoreetmassafeugiatvelNullamloremvelitdignissimsedsemneclobortisauctornisiNullahendreritsemno"
LONG_USERNAME = "LoremipsumdolorsitametconsecteturadipiscingelitPhasellusfeugi"


class UserCreateTestCase(FunctionalTestCase):
    """This class is used to test all inputs and outputs of the POST /user endpoint"""

    # Successful Check
    def test_user_create_success(self):

        request_params = {USERNAME_KEY: TEST_USERNAME, PASSWORD_KEY: TEST_PASSWORD}
        response = self.client.post('/user', data=json.dumps(request_params))

        user = get_user_from_username(TEST_USERNAME)
        self.assertIsNotNone(user, "created user not found")
        self.assertTrue(user.check_hashed_password(TEST_PASSWORD))
        self.check_response_code_and_headers(response, HTTP_CODE_201_CREATED)

    # Input Validation
    def test_user_create_username_too_short_failure(self):
        request_params = {USERNAME_KEY: "no", PASSWORD_KEY: TEST_PASSWORD}
        self.make_and_check_user_create_attempt_with_error(request_params, 901)

    def test_user_create_password_too_short_failure(self):
        request_params = {USERNAME_KEY: TEST_USERNAME, PASSWORD_KEY: "short"}
        self.make_and_check_user_create_attempt_with_error(request_params, 902)

    def test_user_create_password_too_long_failure(self):
        request_params = {USERNAME_KEY: TEST_USERNAME, PASSWORD_KEY: LONG_PASSWORD}
        self.make_and_check_user_create_attempt_with_error(request_params, 903)

    def test_user_create_username_contains_spaces_failures(self):
        request_params = {USERNAME_KEY: "contains spaces", PASSWORD_KEY: TEST_PASSWORD}
        self.make_and_check_user_create_attempt_with_error(request_params, 904)

    def test_user_create_username_too_long_failure(self):
        request_params = {USERNAME_KEY: LONG_USERNAME, PASSWORD_KEY: TEST_PASSWORD}
        self.make_and_check_user_create_attempt_with_error(request_params, 905)

    def make_and_check_user_create_attempt_with_error(self, request_params, app_error_code):
        response = self.client.post('/user', data=json.dumps(request_params))
        user = get_user_from_username(request_params[USERNAME_KEY])
        self.assertIsNone(user)
        self.check_response_code_and_headers(response, HTTP_CODE_422_UNPROCESSABLE_ENTITY)
        self.check_response_contains_only_error(app_error_code, response)

    # Conflict Check
    def test_user_create_username_taken_failure(self):
        user = mock_user()
        self.save_objects(user)
        request_params = {USERNAME_KEY: user.username, PASSWORD_KEY: TEST_PASSWORD}
        response = self.client.post('/user', data=json.dumps(request_params))
        self.check_response_code_and_headers(response, HTTP_CODE_409_CONFLICT)
        self.check_response_contains_only_error(900, response)





