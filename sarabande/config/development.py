import os
from .defaults import Defaults


class Development(Defaults):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.abspath(
        os.path.dirname(__file__)), '../sarabande_development.sqlite3')
