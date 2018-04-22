from .defaults import Defaults


class Test(Defaults):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site_test.sqlite3'
    TESTING = True
