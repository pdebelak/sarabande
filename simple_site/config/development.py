from .defaults import Defaults


class Development(Defaults):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site_development.sqlite3'
    SEND_FILE_MAX_AGE_DEFAULT = 0
