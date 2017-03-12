from . import Form

from wtforms import HiddenField
from wtforms.validators import DataRequired

class VerifyEmailForm(Form):
    verify_email = HiddenField('verify_email', validators = [DataRequired()])
