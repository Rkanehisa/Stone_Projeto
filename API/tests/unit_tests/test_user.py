from unittest import TestCase
from API.models.models import User


class TestUser(TestCase):

    def test_create_user(self):
        username = "Test_User"
        password = "Test_Password"

        user = User(username, password)

        self.assertEqual(user.username, "Test_User")
        self.assertEqual(user.password, "Test_Password")
