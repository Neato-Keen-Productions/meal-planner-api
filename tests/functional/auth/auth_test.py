import json
from tests import FunctionalTestCase
from tests.mocks.user_mock import UserMock, TEST_USERNAME, TEST_PASSWORD

USERNAME_KEY = "username"
PASSWORD_KEY = "password"

class LogInTestCase(FunctionalTestCase):

    def test_login_success(self):
        pass
        # Setup User
        user = UserMock.mock_user()
        # self.save_objects(user)

        # Request is made once in the init
        data = {USERNAME_KEY: TEST_USERNAME, PASSWORD_KEY: TEST_PASSWORD}
        response = self.client.post('/login', data=json.dumps(data))
        # self.check_auth_required(response)

        # # Check response
        # data_dict, error_arr = self.check_response_successful(response)
        # user_dict = data_dict[USER_KEY]
        # UserTests(self).check_full_user(user_dict)
        # self.assertEqual(user.uuid, user_dict[UUID_KEY])
        # self.assertIsNotNone(data_dict[OAUTH_TOKEN_KEY])

    def test_login_fail(self):
        pass
        # Make the request
        # data = {EMAIL_KEY: "test@test.test", PASSWORD_KEY: "wrongpassword"}
        # response = self.client.post('/login', data=json.dumps(data))
        # self.check_auth_required(response)
