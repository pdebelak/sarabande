import re

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_compress import Compress

from .config import Config, BaseModel


app = Flask(__name__)
app.config.from_object(Config)

Compress(app)
db = SQLAlchemy(app, model_class=BaseModel)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)


from .posts import index as post_index, posts as post_blueprint
from .pages import show as page_show, pages as page_blueprint
from .sessions import sessions as session_blueprint
from .users import users as user_blueprint
from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint)
app.register_blueprint(post_blueprint)
app.register_blueprint(page_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(session_blueprint)


def home_page_data(home_page):
    if home_page == 'posts#index':
        return post_index, {}
    elif re.match(r'page#.*', home_page):
        page = home_page.split('#')[1]
        return page_show, {'slug': page}


view_func, defaults = home_page_data(app.config['HOME_PAGE'])
app.route('/', defaults=defaults)(view_func)


from .models import User


@login_manager.user_loader
def login_user(user_id):
    return User.query.get(user_id)
