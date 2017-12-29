from API.models.models import User
from API.tests.base_test import BaseTest


"""
class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.testing = True
        self.app = app.app.test_client()
        with app.app.app_context():
            app.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])"""

class UserTest(BaseTest):
    def test_crud_user(self):
        username = "Test_User"
        password = "Test_Password"

        user = User(username, password)
        self.assertIsNone(User.get_by_username(username))
        user.save_in_db()
        self.assertIsNotNone(User.get_by_username(username))
        user.delete()
        self.assertIsNone(User.get_by_username(username))
