from flask_login import UserMixin

from sarabande import db, bcrypt


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    username = db.Column(db.String, unique=True, nullable=False, index=True)
    user_type = db.Column(db.String, nullable=False, default='commenter')
    password_hash = db.Column(db.String, nullable=False)
    USER_LEVELS = ['admin', 'user', 'commenter']

    def __init__(self, *args, **kwargs):
        if 'password' in kwargs:
            kwargs['password_hash'] = bcrypt.generate_password_hash(
                kwargs['password'])
            del kwargs['password']
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return '<User {username}>'.format(username=self.username)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password)

    def valid_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def authorized_for(self, user_type):
        for level in self.USER_LEVELS:
            if level == self.user_type:
                return True
            if level == user_type:
                return False

    @property
    def is_admin(self):
        return self.user_type == 'admin'

    @property
    def can_post(self):
        return self.authorized_for('user')

    def can_edit(self, user):
        return self.id == user.id or user.is_admin
