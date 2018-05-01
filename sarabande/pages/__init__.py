from flask import Blueprint


pages = Blueprint('page', __name__, template_folder='templates')

from .views import *
