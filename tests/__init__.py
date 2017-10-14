from flask_testing import TestCase

from app import create_app, app

DATA_KEY = "data"
ERRORS_KEY = "errors"


class BaseTestCase (TestCase):
    """TestCase subclass with generic helpers to expedite automated test development"""

    # if the create_app is not implemented NotImplementedError will be raised
    def create_app(self):
        app.config.from_object('config.test_config')
        return app


