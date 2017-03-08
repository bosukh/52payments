import logging
from flask_wtf import FlaskForm as Form
from wtforms import IntegerField, FloatField, StringField, BooleanField, TextAreaField, TextField, SelectMultipleField, HiddenField, PasswordField
from wtforms.validators import Length, Email, DataRequired, EqualTo, URL, Regexp
from flask_wtf.file import FileField
from urlparse import urlparse, urljoin
from flask import request, url_for, session

from urlparse import urlparse, urljoin
from flask import request, url_for, redirect

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_redirect_target():
    logging.debug(request.args.get('next'))
    logging.debug(request.referrer)
    logging.debug(session['initial_referrer'])
    for target in request.args.get('next'), session['initial_referrer'], request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

class RedirectForm(Form):
    next = HiddenField()
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self):
        target = get_redirect_target()
        if target and is_safe_url(target):
            return target
        else:
            return url_for('index') #redirect(self.next.data)

class ReviewForm(Form):
    rating = HiddenField('Rating', validators = [DataRequired()])
    title = StringField('Title', validators = [DataRequired()])
    content = TextAreaField('Your Review', validators = [DataRequired()])

class ForgotPasswordForm(Form):
    first_name = TextField('First Name', validators = [DataRequired(), Regexp(regex='^\w+$')])
    last_name = TextField('Last Name', validators = [DataRequired(), Regexp(regex='^\w+$')])
    email = TextField('Email', validators = [DataRequired(), Length(1, 64), Email()])

class SignUpForm(Form):
    first_name = TextField('First Name', validators = [DataRequired(), Regexp(regex='^\w+$')])
    last_name = TextField('Last Name', validators = [DataRequired(), Regexp(regex='^\w+$')])
    email = TextField('Email', validators = [DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators = [DataRequired(), Length(8, 30), EqualTo('password_2', message='Passwords have to match')])
    password_2 = PasswordField('Re-type Password', validators = [DataRequired(), Length(8, 30), EqualTo('password', message='Passwords have to match')])

class EditInfoForm(Form):
    first_name = TextField('First Name', validators = [Regexp(regex='^\w+$'), DataRequired()])
    last_name = TextField('Last Name', validators = [Regexp(regex='^\w+$'), DataRequired()])
    email = TextField('Email', validators = [Length(1, 64), Email(), DataRequired()])
    phone = TextField('Phone', validators = [Length(10,11)])
    company_name = TextField('Company Name')

class ChangePasswordForm(Form):
    password = PasswordField('New Password', validators = [DataRequired(), Length(8, 30), EqualTo('password_2', message='Passwords have to match')])
    password_2 = PasswordField('Re-type Password', validators = [DataRequired(), Length(8, 30), EqualTo('password', message='Passwords have to match')])

class LoginForm(RedirectForm):
    email = TextField('Email', validators = [DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators = [DataRequired(), Length(8, 30)])

class GoogleLoginForm(RedirectForm):
    id_token = HiddenField('id_token', validators = [DataRequired()])

class SearchForm(Form):
    search_criteria = HiddenField('search_criteria')

class VerifyEmailForm(Form):
    verify_email = HiddenField('verify_email', validators = [DataRequired()])

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
                  ('Mobile', 'Mobile'),
                  ('POS', 'POS'),
                  ('Other', 'Other')]
    pricing_type = [('Tiered', 'Tiered'),
                    ('Interchange Plus', 'Interchange Plus'),
                    ('Flat', 'Flat'),
                    ('Custom', 'Custom'),
                    ('Other', 'Other')]
    title = TextField('Title', validators = [DataRequired()])
    company_profile_name = TextField('Url End Point', validators = [DataRequired()])
    website = TextField('Website', validators = [DataRequired()])
    landing_page = TextField('Landing Page for Apply', validators = [DataRequired()])
    phones = TextAreaField('Phone Numbers With Name (separated by commas)',
                            default= 'General: 000-0000-0000, Customer Service: 000-0000-0000')
    logo_file = FileField('Logo File, 350 x 75 would look the best. (.svg)')
    summary = TextAreaField('Summary (100 Words Limit)')
    full_description = TextAreaField('Full Description')
    year_founded = IntegerField('Year Founded')
    provided_srvs = SelectMultipleField('Provided Services', choices = biz_type)
    complementary_srvs = SelectMultipleField('Complementary Services', choices = srv_type)
    equipment = SelectMultipleField('Equipments', choices = equip_type)
    pricing_method = SelectMultipleField('Pricing Method', choices = pricing_type)
    pricing_range_lower = FloatField('Lower Range For Pricing')
    pricing_range_upper = FloatField('Upper Range For Pricing')
    rate_range_lower = FloatField('Lower Range For Discount Rate')
    rate_range_upper = FloatField('Upper Range For Discount Rate')
    per_transaction_range_lower = FloatField('Lower Range For Per Trasaction')
    per_transaction_range_upper = FloatField('Upper Range For Per Transaction')
