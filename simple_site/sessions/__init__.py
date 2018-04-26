from functools import wraps
from flask import Blueprint, current_app, request
from flask_login import current_user
from flask_login.config import EXEMPT_METHODS

from simple_site.models import User


sessions = Blueprint('sessions', __name__, template_folder='templates')


def login_required(user_type='commenter'):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if request.method in EXEMPT_METHODS:
                return func(*args, **kwargs)
            elif current_app.login_manager._login_disabled:
                return func(*args, **kwargs)
            elif not User.valid_for_type(user_type, current_user):
                return current_app.login_manager.unauthorized()
            return func(*args, **kwargs)
        return decorated_view
    return wrapper


from .views import *
