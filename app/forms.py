from flask_wtf import FlaskForm as Form
from wtforms import IntegerField, FloatField, StringField, BooleanField, TextAreaField, TextField, SelectMultipleField, HiddenField, PasswordField
from wtforms.validators import Length, Email, Required
from flask_wtf.file import FileField

class ReviewForm(Form):
    rating = HiddenField('rating')
    title = StringField('Title')
    content = TextAreaField('Your Review')



class SignUpForm(Form):
    first_name = TextField('First Name')
    last_name = TextField('Last Name')
    email = TextField('Email', validators = [Required(), Length(1, 64), Email()])
    phone = TextField('Phone')
    password = PasswordField('Password')
    password_2 = PasswordField('Re-type Password')

class LoginForm(Form):
    email = TextField('Email')
    password = PasswordField('Password')

class SearchForm(Form):
    search_criteria = HiddenField('search_criteria')

class CompanyForm(Form):
    biz_type = [('Retail','Retail'),
                ('Restaurant','Restaurant'),
                ('E-Commerce', 'E-Commerce'),
                ('Healthcare/Medical', 'Healthcare/Medical'),
                ('Mobile', 'Mobile'),
                ('Professional/Personal Services', 'Professional/Personal Services'),
                ('Non-Profit', 'Non-Profit'),
                ('High-Risk', 'High-Risk'),
                ('High-Volume', 'High-Volume'),
                ('Other', 'Other')]
    srv_type = [('Marketing', 'Marketing'),
                ('Analytics', 'Analytics'),
                ('Recurling Bill', 'Recurling Bill'),
                ('Chargeback', 'Chargeback'),
                ('Security', 'Security'),
                ('Other', 'Other')]
    equip_type = [('Verifone','Verifone'),
                  ('Ingenico', 'Ingenico'),
                  ('Other', 'Other')]
    pricing_type = [('Tiered', 'Tiered'),
                    ('Interchange Plus', 'Interchange Plus'),
                    ('Flat', 'Flat'),
                    ('Custom', 'Custom')
                    ]
    title = TextField('Title')
    company_profile_name = TextField('Url End Point')
    logo_file = FileField('Logo File (.svg)')
    summary = TextAreaField('Summary (100 Words Limit)')
    full_description = TextAreaField('Full Description')
    year_founded = IntegerField('Year Founded')
    provided_srvs = SelectMultipleField('Provided Services', choices = biz_type)
    complementary_srvs = SelectMultipleField('Complementary Services', choices = srv_type)
    equipment = SelectMultipleField('Equipments', choices = equip_type)
    pricing_method = SelectMultipleField('Pricing Method', choices = pricing_type)
    pricing_range_lower = FloatField('Lower Range For Pricing')
    pricing_range_upper = FloatField('Upper Range For Pricing')
