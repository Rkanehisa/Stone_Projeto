from API.models.models import Card, User
from API.tests.base_test import BaseTest


class TestUser(BaseTest):

    def test_create_user(self):
        username = "Test_User"
        password = "Test_Password"
        name = "Test User"
        number = "0000 0000 0000 0000"
        ccv = "000"
        due_date = "2017/08/15"
        expiration_date = "2023/08/15"
        limit = 5000

        user = User(username, password)
        user.save_in_db()

        card = Card(user.username, name, number, ccv, due_date, expiration_date, limit)

        self.assertEqual(user.id, card.user_id)
