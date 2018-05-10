from .user_config import user_config


class Defaults(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TITLE = user_config['title']
    DESCRIPTION = user_config.get('description')
    HOME_PAGE = user_config.get('home_page', '/posts')
    NAV_LINKS = user_config.get('nav_links', [])
    SECRET_KEY = user_config['secret_key']
    COPYRIGHT = user_config.get('copyright')
    THEME = user_config.get('theme')
    TWITTER_USER = user_config.get('twitter_user')
