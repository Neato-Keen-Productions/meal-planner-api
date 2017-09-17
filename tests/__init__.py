from flask_testing import TestCase
from app import app


class BaseTestCase (TestCase):
    """TestCase subclass with generic helpers to expedite automated test development"""

    # if the create_app is not implemented NotImplementedError will be raised
    def create_app(self):
        # app.config.from_object('api.test_config')
        # app.config['TESTING'] = True

        return app


class FunctionalTestCase (BaseTestCase):
    pass
