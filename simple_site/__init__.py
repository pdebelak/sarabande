from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from .config import Config


app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

from .models import *
from .posts import posts, index
app.register_blueprint(posts)


app.route('/')(index)
