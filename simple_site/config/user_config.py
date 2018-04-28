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


config_filename = os.getenv('SITE_CONFIG', 'example_config.yml')
try:
    with open(config_filename) as config_file:
        user_config = UserConfig(yaml.load(config_file))
except IOError:
    raise RuntimeError(
        'Unable to open config file {file}'.format(file=config_filename))
