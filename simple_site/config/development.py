from .defaults import Defaults


class Development(Defaults):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site_development.sqlite3'
