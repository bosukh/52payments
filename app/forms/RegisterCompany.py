from . import Form

from flask_wtf.file import FileField
from wtforms import StringField, TextAreaField, FileField, SelectMultipleField
from wtforms.validators import DataRequired

class RegisterCompanyForm(Form):
    biz_type = []
    srv_type = []
    equip_type = []
    pricing_type = [('Tiered', 'Tiered'),
                    ('Interchange Plus', 'Interchange Plus'),
                    ('Flat', 'Flat'),
                    ('Custom', 'Custom'),
                    ('Other', 'Other')]
    title = StringField('Title', validators = [DataRequired()])
    company_profile_name = StringField('Url End Point', validators = [DataRequired()])
    website = StringField('Website', validators = [DataRequired()])
    landing_page = StringField('Landing Page for Apply', validators = [DataRequired()])
    phones = TextAreaField('Phone Numbers With Name (separated by commas)',
                            default= 'General: 000-0000-0000, Customer Service: 000-0000-0000')
    logo_file = FileField('Logo File, 350 x 75 would look the best. (.png)')
    meta_description = StringField('Summary (160 Words Limit)')
    full_description = TextAreaField('Full Description')
    year_founded = StringField('Year Founded')
    provided_srvs = SelectMultipleField('Provided Services', choices = biz_type)
    complementary_srvs = SelectMultipleField('Complementary Services', choices = srv_type)
    equipment = SelectMultipleField('Equipments', choices = equip_type)
    pricing_method = SelectMultipleField('Pricing Method', choices = pricing_type)
