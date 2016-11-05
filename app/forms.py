from flask_wtf import FlaskForm as Form
from wtforms import FloatField, StringField, BooleanField, TextAreaField, TextField, SelectMultipleField, HiddenField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField

class SearchForm(Form):
    retail = BooleanField('Retail', default=False)
    restuarant = BooleanField('Restuarant', default=False)
    e_commerce = BooleanField('E-Commerce', default=False)
    healthcare_medical = BooleanField('Healthcare/Medical', default=False)
    mobile = BooleanField('Mobile', default=False)
    prof_personal_srv = BooleanField('Professional/Personal Services', default=False)
    non_profit = BooleanField('Non-Profit', default=False)
    high_risk = BooleanField('High-Risk', default=False)
    high_volume = BooleanField('High-Volume', default=False)
    other = BooleanField('Other', default=False)

class CompanyForm(Form):
    biz_type = [('Retail','Retail'),
                ('Restuarant','Restuarant'),
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
    title = TextField('Title')
    company_profile_name = TextField('Url End Point')
    logo_file = FileField('Logo File (.svg)')
    summary = TextAreaField('Summary (300 Words Limit)')
    full_description = TextAreaField('Full Description')
    year_founded = FloatField('Year Founded')
    provided_srvs = SelectMultipleField('Provided Services', choices = biz_type)
    complementary_srvs = SelectMultipleField('Complementary Services', choices = srv_type)
    equipment = SelectMultipleField('Equipments', choices = equip_type)
