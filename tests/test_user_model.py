import unittest

from simple_site.models import User


class TestUserModel(unittest.TestCase):
    def testPasswordHashSet(self):
        user = User(password='hello')
        self.assertTrue(user.password_hash)

    def testPasswordHashAuthenticates(self):
        user = User(password='hello')
        self.assertTrue(user.valid_password('hello'))
        self.assertFalse(user.valid_password('goodbye'))

    def testRepr(self):
        user = User(username='Peter Pebelak')
        self.assertEqual(str(user), '<User Peter Pebelak>')
