from app.models.user import User

TEST_USERNAME = "test_username"
TEST_PASSWORD = "test_password"


def mock_user():
    return User(TEST_USERNAME, TEST_PASSWORD)
