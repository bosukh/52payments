from . import Form

from wtforms import StringField
from wtforms.validators import Length, Email, DataRequired, Regexp

class EditInfoForm(Form):
    first_name = StringField('First Name', validators = [Regexp(regex='^\w+$'), DataRequired()])
    last_name = StringField('Last Name', validators = [Regexp(regex='^\w+$'), DataRequired()])
    email = StringField('Email', validators = [Length(1, 64), Email(), DataRequired()])
    phone = StringField('Phone', validators = [Length(10,11), Regexp(regex='^\d+$')])
    company_name = StringField('Company Name')
