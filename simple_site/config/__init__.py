import os

from .test import Test
from .development import Development
from .production import Production
from .base_model import BaseModel


ENV = os.getenv('SITE_ENV', 'development')


_configs = {
    'test': Test,
    'development': Development,
    'production': Production,
}

Config = '{name}.{config}'.format(name=__name__, config=_configs[ENV].__name__)
