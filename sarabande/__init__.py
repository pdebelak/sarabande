from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_compress import Compress
from flask_migrate import Migrate

from .assets import Assets
from .config import Config, BaseModel
from .helpers import safe_return_to


app = Flask(__name__)
app.config.from_object(Config)

Compress(app)
Assets(app)
db = SQLAlchemy(app, model_class=BaseModel)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)


from .posts import posts as post_blueprint
from .images import images as image_blueprint
from .sessions import sessions as session_blueprint
from .users import users as user_blueprint
from .pages import pages as page_blueprint
from .tags import tags as tag_blueprint
from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint)
app.register_blueprint(image_blueprint)
app.register_blueprint(post_blueprint)
app.register_blueprint(tag_blueprint)
app.register_blueprint(user_blueprint)
app.register_blueprint(page_blueprint)
app.register_blueprint(session_blueprint)
from .views import license, home_page
from .filters import publish_time, comment_time
from .errors import *
