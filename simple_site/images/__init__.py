from flask import Blueprint


images = Blueprint('images', __name__, template_folder='templates')

from .views import *
