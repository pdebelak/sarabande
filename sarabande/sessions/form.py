from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

from sarabande.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    def validate(self):
        if not super(LoginForm, self).validate():
            return False
        user = User.query.filter(User.username == self.username.data).first()
        if user is None:
            self.username.errors.append('Unknown username')
            return False
        if not user.valid_password(self.password.data):
            self.password.errors.append('Invalid password')
            return False

        self.user = user
        return True
