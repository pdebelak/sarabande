from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Optional

from simple_site.models import User


class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password')
    user_type = SelectField(
        'User type',
        choices=[
            ('commenter', 'Commenter'),
            ('user', 'User'),
            ('admin', 'Admin')],
        validators=[Optional()])

    def to_user(self):
        user = User(
            username=self.username.data,
            password=self.password.data,
        )
        if self.user_type.data != 'None':
            user.user_type = self.user_type.data
        return user

    def update_user(self, user):
        user.username = self.username.data
        if self.password.data:
            user.set_password(self.password.data)
        if self.user_type.data:
            user.user_type = self.user_type.data

    def validate(self, current_user, user=None):
        if not super(UserForm, self).validate():
            return False
        if user is None and not self.password.data:
            self.password.errors.append('This field is required.')
            return False
        if not (current_user.is_authenticated and current_user.is_admin) \
                and self.user_type.data != 'None':
            return False
        return True
