from functools import wraps
from flask import Blueprint
from flask_login import current_user, login_required as original_login_required

from sarabande import login_manager
from sarabande.models import User


sessions = Blueprint('sessions', __name__, template_folder='templates')


def login_required(user_type='commenter'):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_user.is_authenticated \
                    and not current_user.authorized_for(user_type):
                return login_manager.unauthorized()
            else:
                return original_login_required(func)(*args, **kwargs)
        return decorated_view
    return wrapper


@login_manager.user_loader
def login_user(user_id):
    return User.query.get(user_id)


from .views import *
