import json
from tests import FunctionalTestCase
from tests.mocks.user_mock import mock_user, TEST_USERNAME, TEST_PASSWORD


USERNAME_KEY = "username"
PASSWORD_KEY = "password"
AUTH_TOKEN_KEY = "auth_token"


class LogInTestCase(FunctionalTestCase):

    def test_login_success(self):

        # Setup User
        user = mock_user()
        self.save_objects(user)

        # Request is made once in the init
        data = {USERNAME_KEY: TEST_USERNAME, PASSWORD_KEY: TEST_PASSWORD}
        response = self.client.post('/login', data=json.dumps(data))

        # Check response
        self.check_response_success_and_headers(response)
        self.check_errors_not_in_response(response)
        data_dict = self.unpack_extant_response_data(response)
        auth_token = data_dict[AUTH_TOKEN_KEY]
        self.assertIsNotNone(auth_token)

    # Invalid Login Parameter Tests
    def test_login_invalid_password_failure(self):

        # Setup User
        user = mock_user()
        self.save_objects(user)

        # Make the request
        data = {USERNAME_KEY: TEST_USERNAME, PASSWORD_KEY: "incorrect_password"}
        self.make_and_check_invalid_data_login_attempt(data)

    def test_login_invalid_username_failure(self):
        data = {USERNAME_KEY: "incorrect_username", PASSWORD_KEY: TEST_PASSWORD}
        self.make_and_check_invalid_data_login_attempt(data)

    def make_and_check_invalid_data_login_attempt(self, data):
        response = self.client.post('/login', data=json.dumps(data))

        # Check the response
        self.check_response_code(response, 200)
        self.check_response_headers_content_type(response)
        self.check_request_contains_only_auth_error(response)

    # Missing Login Parameter Tests
    def test_login_missing_username_failure(self):
        data = {PASSWORD_KEY: TEST_PASSWORD}
        self.make_and_check_missing_data_login_attempt(data)

    def test_login_missing_password_failure(self):
        data = {USERNAME_KEY: TEST_USERNAME}
        self.make_and_check_missing_data_login_attempt(data)

    def make_and_check_missing_data_login_attempt(self, data):
        response = self.client.post('/login', data=json.dumps(data))

        # Check the response
        self.check_response_code(response, 200)
        self.check_response_headers_content_type(response)
        self.check_request_contains_only_missing_parameter_error(response)
