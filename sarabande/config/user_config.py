import os
import yaml


class UserConfig(object):
    def __init__(self, user_config):
        self.user_config = user_config

    def __getitem__(self, item):
        try:
            return self.user_config[item]
        except KeyError:
            raise RuntimeError(
                '{item} not listed in config file'.format(item=item))

    def get(self, item, default=None):
        return self.user_config.get(item, default)


def open_user_config(config_filename):
    try:
        with open(config_filename) as config_file:
            return UserConfig(yaml.load(config_file))
    except IOError:
        raise RuntimeError(
            'Unable to open config file {file}'.format(file=config_filename))


config_filename = os.getenv('SARABANDE_CONFIG', 'example_config.yml')
user_config = open_user_config(config_filename)
