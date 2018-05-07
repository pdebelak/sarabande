import unittest

from sarabande.config.user_config import UserConfig, open_user_config


class TestUserConfig(unittest.TestCase):
    def setUp(self):
        self.config = UserConfig({'found': 'yes'})

    def testFoundGetItem(self):
        self.assertEqual(self.config['found'], 'yes')

    def testNotFoundGetItem(self):
        with self.assertRaises(RuntimeError,
                               msg='other not listed in config file'):
            self.config['other']

    def testFoundGet(self):
        self.assertEqual(self.config.get('found'), 'yes')

    def testNotFoundGet(self):
        self.assertIsNone(self.config.get('other'))

    def testOpenUserConfigFound(self):
        user_config = open_user_config('example_config.yml')
        self.assertTrue(user_config)

    def testOpenUserConfigNotFound(self):
        with self.assertRaises(
                RuntimeError,
                msg='Unable to open config file non_existant.yml'):
            open_user_config('non_existant.yml')
