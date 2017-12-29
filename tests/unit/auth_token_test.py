from tests import BaseTestCase
from app.models.auth_token import AuthToken
from app.controllers.auth_token import AuthTokenStatus
import datetime
import re

IDENTIFIER = "f7316c09-3774-41ae-8f3c-2a5bb3f1f165"
ALTERNATE_IDENTIFER = "233deged-2532-131d-dad3-fge135dsa32s"


class AuthTokenTestCase (BaseTestCase):

    def test_each_auth_token_for_one_user_is_unique(self):
        """
        Each token is generated with an expiration time.  However,
        this is only reflected down to the minute so two different time
        deltas must be used or the same token could be generated
        """
        first_token = AuthToken(IDENTIFIER, datetime.timedelta(minutes=5))
        second_token = AuthToken(IDENTIFIER, datetime.timedelta(minutes=6))
        self.assertNotEqual(first_token, second_token, "Auth tokens for the same user must be unique")

    def test_auth_tokens_with_different_subjects_are_unique(self):
        first_token = AuthToken(IDENTIFIER, datetime.timedelta(days=5))
        second_token = AuthToken(ALTERNATE_IDENTIFER, datetime.timedelta(seconds=5))
        self.assertNotEqual(first_token, second_token, "Auth tokens for different users must be unique")

    def test_auth_token_decrypted_subject_is_same_as_pre_encryped_subject(self):
        initial_subject = IDENTIFIER
        auth_token = AuthToken(initial_subject, datetime.timedelta(days=5))
        self.assertEquals(initial_subject, auth_token.subject, "Decoded subject must match initial subject.\nInitial: " + initial_subject + "\nDecoded: " + auth_token.subject)

    def test_auth_token_for_correct_jwt_format(self):
        """
        Each JWT token must have a header, body, and signature separated by period characters
        """
        auth_token = AuthToken(IDENTIFIER, datetime.timedelta(days=5))
        match = re.match(r'(.*)\.(.*)\.(.*)', auth_token.encoded_value, re.M | re.I)
        self.assertIsNotNone(match)

    def test_auth_token_past_expiration(self):
        auth_token = AuthToken(IDENTIFIER, datetime.timedelta(days=-5))
        self.assertEqual(auth_token.status, AuthTokenStatus.EXPIRED)

    def test_auth_token_invalid_signature_returns_error(self):
        auth_token = AuthToken(encoded_value="Bad.Auth.Token")
        self.assertEqual(auth_token.status, AuthTokenStatus.INVALID)
