from API.models.models import User, Card
from API.tests.base_test import BaseTest


class CardTest(BaseTest):
    def testCrudCard(self):
        username = "Test_User"
        password = "Test_Password"
        name = "Test User"
        number = "0000 0000 0000 0000"
        ccv = "000"
        due_date = "2017/08/15"
        expiration_date = "2023/08/15"
        limit = 5000

        user = User(username, password)

        self.assertIsNone(User.get_by_username(username))
        user.save_in_db()
        self.assertIsNotNone(User.get_by_username(username))

        card = Card(user.username, name, number, ccv, due_date, expiration_date, limit)
        card.save_in_db()

        self.assertIsNotNone(Card.get_by_number(card.number))

        user.delete()
        self.assertIsNone(User.get_by_username(username))

        self.assertIsNone(Card.get_by_number(card.number))