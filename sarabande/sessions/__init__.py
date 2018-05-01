from functools import wraps
from flask import Blueprint, request
from flask_login import current_user
from flask_login.config import EXEMPT_METHODS

from sarabande import login_manager


sessions = Blueprint('sessions', __name__, template_folder='templates')


def login_required(user_type='commenter'):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if request.method in EXEMPT_METHODS:
                return func(*args, **kwargs)
            elif not current_user.is_authenticated \
                    or not current_user.authorized_for(user_type):
                return login_manager.unauthorized()
            return func(*args, **kwargs)
        return decorated_view
    return wrapper


from .views import *
