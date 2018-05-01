from .defaults import Defaults
from .user_config import user_config


class Production(Defaults):
    SQLALCHEMY_DATABASE_URI = user_config['database_uri']
