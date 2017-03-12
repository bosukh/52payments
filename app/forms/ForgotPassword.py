from . import Form
from wtforms import StringField
from wtforms.validators import Length, Email, DataRequired, Regexp

class ForgotPasswordForm(Form):
    first_name = StringField('First Name', validators = [DataRequired(), Regexp(regex='^\w+$')])
    last_name = StringField('Last Name', validators = [DataRequired(), Regexp(regex='^\w+$')])
    email = StringField('Email', validators = [DataRequired(), Length(1, 64), Email()])
