from unittest import TestCase
from API.models.wallet import Wallet


class TestUser(TestCase):

    def test_create_wallet(self):
        user = "Teste"

        wallet = Wallet(user)

        self.assertEqual(wallet.user.username, "Teste")
        self.assertEqual(wallet.limit, 0)
