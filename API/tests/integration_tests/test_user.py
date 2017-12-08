from unittest import TestCase
from API.models.user import User
import os


class TestUser(TestCase):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL', 'sqlite:///tests//database.db')

    def setUp(self):
        from API.app import app

        self.app = app
        self.app_context = app.app_context()
        self.app["DEBUG"] = True
        self.app["TESTING"] = True


    def test_user(self):
        pass
