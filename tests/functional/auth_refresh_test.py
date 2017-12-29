from tests.functional import FunctionalTestCase
from tests.mocks.user_mock import mock_user

from app.models.auth_token import AuthToken
from app.constants.status_codes import *
import datetime


endpoint = '/auth_token/refresh'


class AuthRequiredTestCase (FunctionalTestCase):

    def test_auth_refresh_passes_with_valid_user(self):
        # Setup Mocks
        user = mock_user()
        self.save_objects(user)
        auth_token = AuthToken(user.uuid, datetime.timedelta(days=30))

        # Make Request
        header = {'Cookie': str("auth_token=" + auth_token.encoded_value)}
        response = self.client.get(endpoint, headers=header)

        # Validate Results
        self.check_response_code_and_headers(response, HTTP_CODE_200_OK)
        self.check_errors_not_in_response(response)

        # Check Cookie
        self.assertIn('Set-Cookie', response.headers.keys())
        cookie_value = response.headers['Set-Cookie']
        self.assertIn('auth_token', cookie_value)
        self.assertIn('Domain', cookie_value)
        self.assertIn('Expires', cookie_value)
        self.assertIn('HttpOnly', cookie_value)
        self.assertIn('Path', cookie_value)

    def test_auth_refesh_fails_without_token(self):
        # Make Request
        response = self.client.get(endpoint)

        # Validate Results
        self.check_response_code_and_headers(response, HTTP_CODE_401_UNAUTHORIZED)
        self.check_response_contains_only_error(HTTP_CODE_401_UNAUTHORIZED, response)

    def test_auth_refresh_fails_with_expired_token(self):
        # Setup Mocks
        user = mock_user()
        self.save_objects(user)
        auth_token = AuthToken(user.uuid, datetime.timedelta(days=-30))

        # Make Request
        header = {'Cookie': str("auth_token=" + auth_token.encoded_value)}
        response = self.client.get(endpoint, headers=header)

        # Validate Results
        self.check_response_code_and_headers(response, HTTP_CODE_401_UNAUTHORIZED)
        self.check_response_contains_only_error(HTTP_CODE_401_UNAUTHORIZED, response)

    def test_auth_refresh_fails_with_invalid_token(self):
        # Make Request
        header = {'Cookie': "auth_token=Invalid.Token"}
        response = self.client.get(endpoint, headers=header)

        # Validate Results
        self.check_response_code_and_headers(response, HTTP_CODE_401_UNAUTHORIZED)
        self.check_response_contains_only_error(HTTP_CODE_401_UNAUTHORIZED, response)

    def test_auth_refresh_fails_with_blacklisted_user(self):
        # Setup Mocks
        user = mock_user()
        user.is_blacklisted = True
        self.save_objects(user)
        auth_token = AuthToken(user.uuid, datetime.timedelta(days=30))

        # Make Request
        header = {'Cookie': str("auth_token=" + auth_token.encoded_value)}
        response = self.client.get(endpoint, headers=header)

        # Validate Results
        self.check_response_code_and_headers(response, HTTP_CODE_403_FORBIDDEN)
        self.check_response_contains_only_error(HTTP_CODE_403_FORBIDDEN, response)

    def test_auth_refresh_fails_without_valid_user(self):
        # Setup Mocks
        auth_token = AuthToken("Invalid UUID", datetime.timedelta(days=30))

        # Make Request
        header = {'Cookie': str("auth_token=" + auth_token.encoded_value)}
        response = self.client.get(endpoint, headers=header)

        # Validate Results
        self.check_response_code_and_headers(response, HTTP_CODE_401_UNAUTHORIZED)
        self.check_response_contains_only_error(HTTP_CODE_404_NOT_FOUND, response)
