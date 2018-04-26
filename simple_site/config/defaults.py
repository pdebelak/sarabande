from .user_config import user_config


class Defaults:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TITLE = user_config['title']
    HOME_PAGE = user_config.get('home_page', 'posts#index')
    NAV_LINKS = user_config.get('nav_links', [])
    SECRET_KEY = user_config['secret_key']
