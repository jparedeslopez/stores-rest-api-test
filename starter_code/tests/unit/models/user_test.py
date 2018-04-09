from ....models.user import UserModel
from ..unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def init_test(self):
        user = UserModel('test_user', 'test_pass')

        self.assertEqual(user.username, 'test_user')
        self.assertEqual(user.password, 'test_pass')