from . import RedirectForm

from wtforms import HiddenField
from wtforms.validators import DataRequired

class GoogleLoginForm(RedirectForm):
    id_token = HiddenField('id_token', validators = [DataRequired()])
