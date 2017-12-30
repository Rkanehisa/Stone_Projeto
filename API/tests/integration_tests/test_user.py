from API.models.models import User
from API.tests.base_test import BaseTest


class UserTest(BaseTest):
    def testCrudUser(self):
        username = "Test_User"
        password = "Test_Password"

        user = User(username, password)
        self.assertIsNone(User.get_by_username(username))
        user.save_in_db()
        self.assertIsNotNone(User.get_by_username(username))
        user.delete()
        self.assertIsNone(User.get_by_username(username))
