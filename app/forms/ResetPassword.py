from . import Form

from wtforms import PasswordField
from wtforms.validators import Length, DataRequired, EqualTo

class ResetPasswordForm(Form):
    password = PasswordField('New Password', validators = [DataRequired(), Length(8, 30), EqualTo('password_2', message='Passwords have to match')])
    password_2 = PasswordField('Re-type Password', validators = [DataRequired(), Length(8, 30), EqualTo('password', message='Passwords have to match')])
