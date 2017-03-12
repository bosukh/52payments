from . import Form
from wtforms import StringField, TextAreaField, HiddenField
from wtforms.validators import DataRequired #Length, Email, Regexp

class WriteReviewForm(Form):
    rating = HiddenField('Rating', validators = [DataRequired()])
    title = StringField('Title', validators = [DataRequired()])
    content = TextAreaField('Your Review', validators = [DataRequired()])
    #first_name = StringField('First Name', validators = [DataRequired(), Regexp(regex='^\w+$')])
    #last_name = StringField('Last Name', validators = [DataRequired(), Regexp(regex='^\w+$')])
    #email = StringField('Email', validators = [DataRequired(), Length(1, 64), Email()])
