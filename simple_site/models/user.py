from flask_login import UserMixin

from simple_site import db, bcrypt


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    username = db.Column(db.String, unique=True, nullable=False, index=True)
    user_type = db.Column(db.String, nullable=False, default='commenter')
    password_hash = db.Column(db.String, nullable=False)

    def __init__(self, *args, **kwargs):
        if 'password' in kwargs:
            kwargs['password_hash'] = bcrypt.generate_password_hash(
                kwargs['password'])
            del kwargs['password']
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<User {username}>'.format(username=self.username)

    def valid_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def valid_for_type(user_type, user):
        if not user.is_authenticated:
            return False
        type_mapping = {
            'commenter': ['commenter', 'user', 'admin'],
            'user': ['user', 'admin'],
            'admin': ['admin'],
        }
        return user.user_type in type_mapping[user_type]
