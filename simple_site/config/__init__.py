import os

from .test import Test
from .development import Development
from .production import Production


ENV = os.getenv('SITE_ENV', 'development')


configs = {
    'test': Test,
    'development': Development,
    'production': Production,
}

Config = '{name}.{config}'.format(name=__name__, config=configs[ENV].__name__)
