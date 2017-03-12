from . import RedirectForm

from wtforms import StringField, PasswordField
from wtforms.validators import Length, DataRequired, Email

class LoginForm(RedirectForm):
    email = StringField('Email', validators = [DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators = [DataRequired(), Length(8, 30)])
