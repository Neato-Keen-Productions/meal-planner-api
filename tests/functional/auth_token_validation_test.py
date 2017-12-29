from tests.functional import FunctionalTestCase
from app.controllers.auth_token.validate_auth_token_service import valid_user_from_auth_token
from app.models.auth_token import AuthToken
from tests.mocks.user_mock import mock_user
import datetime

IDENTIFIER = "f7316c09-3774-41ae-8f3c-2a5bb3f1f165"
ALTERNATE_IDENTIFER = "233deged-2532-131d-dad3-fge135dsa32s"


class AuthTokenValidationTestCase (FunctionalTestCase):

    def test_auth_validation_for_non_blacklisted_user_is_valid(self):
        # Setup Mocks
        user = mock_user()
        user.is_blacklisted = False
        self.save_objects(user)
        auth_token = AuthToken(user.uuid, datetime.timedelta(days=30))

        # Run Function
        found_user, error = valid_user_from_auth_token(auth_token)

        # Validate Results
        self.assertIsNotNone(found_user, "A valid, non-blacklisted user should be found when using a valid token")
        self.assertIsNone(error, "A valid, non-blacklisted user token should not generate an error")

    def test_auth_validation_for_incorrectly_formatted_token_is_invalid(self):
        # Setup Mocks
        auth_token = AuthToken(encoded_value="Invalid Token")

        # Run Function
        found_user, error = valid_user_from_auth_token(auth_token)

        # Validate Results
        self.assertIsNone(found_user, "A user should not be returned from an invalid token")
        self.assertEqual(error.code, 401, "Invalid token error code should be 401 Unauthorized")

    def test_auth_validation_for_expired_token_is_invalid(self):
        # Setup Mocks
        user = mock_user()
        auth_token = AuthToken(user.uuid, datetime.timedelta(days=-30))

        # Run Function
        found_user, error = valid_user_from_auth_token(auth_token)

        # Validate Results
        self.assertIsNone(found_user, "A user should not be returned from an expired token")
        self.assertEqual(error.code, 401, "Expired token error code should be 401 Unauthorized")

    def test_auth_validation_for_blacklisted_users_is_invalid(self):
        # Setup Mocks
        user = mock_user()
        user.is_blacklisted = True
        self.save_objects(user)
        auth_token = AuthToken(user.uuid, datetime.timedelta(days=30))

        # Run Function
        found_user, error = valid_user_from_auth_token(auth_token)

        # Validate Results
        self.assertIsNone(found_user, "A user should not be returned when blacklisted")
        self.assertEqual(error.code, 403, "Blacklisting error code should be 403 Forbidden")

    def test_auth_validation_for_not_found_user_is_invalid(self):
        auth_token = AuthToken("1234-1234-1234", datetime.timedelta(days=30))

        # Run Function
        found_user, error = valid_user_from_auth_token(auth_token)

        # Validate Results
        self.assertIsNone(found_user, "A user that is not found should not be returned")
        self.assertEqual(error.code, 404, "User not found error code should be 404 Not Found")
