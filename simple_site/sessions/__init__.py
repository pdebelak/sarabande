from flask import Blueprint


sessions = Blueprint('sessions', __name__, template_folder='templates')

from .views import *
