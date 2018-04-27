from flask_login import UserMixin

from simple_site import db, bcrypt


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    username = db.Column(db.String, unique=True, nullable=False, index=True)
    user_type = db.Column(db.String, nullable=False, default='commenter')
    password_hash = db.Column(db.String, nullable=False)
    USER_LEVELS = {
        'commenter': 0,
        'user': 1,
        'admin': 2,
    }

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

    def authorized_for(self, user_type):
        return self.USER_LEVELS[self.user_type] >= self.USER_LEVELS[user_type]

    @property
    def is_admin(self):
        return self.user_type == 'admin'

    @property
    def is_commenter(self):
        return self.user_type == 'commenter'
