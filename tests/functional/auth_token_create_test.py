import json

from tests.functional import FunctionalTestCase
from tests.functional.constant_keys import USERNAME_KEY, PASSWORD_KEY, AUTH_TOKEN_KEY
from tests.mocks.user_mock import mock_user, TEST_USERNAME, TEST_PASSWORD
from app.constants.status_codes import HTTP_CODE_200_OK, HTTP_CODE_401_UNAUTHORIZED

endpoint = '/auth_token'


class AuthTokenCreateTestCase(FunctionalTestCase):

    def test_auth_token_create_success(self):

        # Setup User
        user = mock_user()
        self.save_objects(user)

        # Make Request
        data = {USERNAME_KEY: TEST_USERNAME, PASSWORD_KEY: TEST_PASSWORD}
        response = self.client.post(endpoint, data=json.dumps(data))

        # Check Response
        self.check_response_code_and_headers(response, HTTP_CODE_200_OK)
        self.check_errors_not_in_response(response)
        data_dict = self.unpack_extant_response_data(response)
        auth_token = data_dict[AUTH_TOKEN_KEY]
        self.assertIsNotNone(auth_token)

        # Check Cookie
        self.assertIn('Set-Cookie', response.headers.keys())
        cookie_value = response.headers['Set-Cookie']
        self.assertIn('auth_token', cookie_value)
        self.assertIn('Domain', cookie_value)
        self.assertIn('Expires', cookie_value)
        self.assertIn('HttpOnly', cookie_value)
        self.assertIn('Path', cookie_value)

    # Invalid Login Parameter Tests
    def test_auth_token_create_invalid_password_failure(self):

        # Setup User
        user = mock_user()
        self.save_objects(user)

        # Make the request
        data = {USERNAME_KEY: TEST_USERNAME, PASSWORD_KEY: "incorrect_password"}
        self.make_and_check_invalid_data_auth_token_create_attempt(data)

    def test_auth_token_create_invalid_username_failure(self):
        data = {USERNAME_KEY: "incorrect_username", PASSWORD_KEY: TEST_PASSWORD}
        self.make_and_check_invalid_data_auth_token_create_attempt(data)

    def make_and_check_invalid_data_auth_token_create_attempt(self, data):
        response = self.client.post(endpoint, data=json.dumps(data))

        # Check the response
        self.check_response_code(response, HTTP_CODE_401_UNAUTHORIZED)
        self.check_response_headers_content_type(response)

    # Missing Login Parameter Tests
    def test_auth_token_create_missing_username_failure(self):
        data = {PASSWORD_KEY: TEST_PASSWORD}
        self.make_and_check_missing_data_auth_token_create_attempt(data)

    def test_auth_token_create_missing_password_failure(self):
        data = {USERNAME_KEY: TEST_USERNAME}
        self.make_and_check_missing_data_auth_token_create_attempt(data)

    def make_and_check_missing_data_auth_token_create_attempt(self, data):
        response = self.client.post(endpoint, data=json.dumps(data))

        # Check the response
        self.check_response_code(response, HTTP_CODE_200_OK)
        self.check_response_headers_content_type(response)
        self.check_response_contains_only_missing_parameter_error(response)
