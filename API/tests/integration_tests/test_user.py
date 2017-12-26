from unittest import TestCase
from API.models.models import User
import os


class TestUser(TestCase):

    def setUp(self):
        from API.app import app

        self.app = app
        self.app_context = app.app_context()


    def test_user(self):
        pass
