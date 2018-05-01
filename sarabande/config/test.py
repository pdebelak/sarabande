from .defaults import Defaults


class Test(Defaults):
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
