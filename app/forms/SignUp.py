from . import Form

from wtforms import StringField, PasswordField
from wtforms.validators import Length, Email, DataRequired, Regexp, EqualTo


class SignUpForm(Form):
    first_name = StringField('First Name', validators = [DataRequired(), Regexp(regex='^\w+$')])
    last_name = StringField('Last Name', validators = [DataRequired(), Regexp(regex='^\w+$')])
    email = StringField('Email', validators = [DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators = [DataRequired(), Length(8, 30), EqualTo('password_2', message='Passwords have to match')])
    password_2 = PasswordField('Re-type Password', validators = [DataRequired(), Length(8, 30), EqualTo('password', message='Passwords have to match')])
