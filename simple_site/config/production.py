import os

from .defaults import Defaults


class Production(Defaults):
    SQLALCHEMY_DATABASE_URI = os.getenv('SITE_DATABASE_URI')
