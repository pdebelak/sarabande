from .defaults import Defaults


class Test(Defaults):
    TESTING = True
    WTF_CSRF_ENABLED = False
