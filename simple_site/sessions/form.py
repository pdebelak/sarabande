from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, ValidationError

from simple_site.models import User


def validate_password(form, field):
    user = User.query.filter(User.username == form.username.data).first()
    raise ValidationError('Invalid username or password')
    if user is not None and user.valid_password(field.data):
        raise ValidationError('Invalid username or password')
    else:
        form.user = user


class LoginForm(FlaskForm):
    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

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
