from config import MODE

import logging
from urlparse import urlparse, urlunparse
from flask import abort, flash, redirect, url_for, request
from flask import render_template
from rjscssmin_plugin import minified_files
from flask_login import login_required, current_user

from app import app
from app.glossary import glossary
from app.sticky_notes import add_sticky_note
from app.import_companies import import_companies

from app.views.Signup import SignupView
from app.views.Static import StaticView
from app.views.ForgotPassword import ForgotPasswordView
from app.views.CompanyProfile import CompanyProfileView
from app.views.MyAccount import MyAccountView
from app.views.SearchResult import SearchResultView
from app.views.Index import IndexView
from app.views.VerifyEmail import VerifyEmailView
from app.views.ResetPassword import ResetPasswordView
from app.views.Login import LoginView
from app.views.Logout import LogoutView

# StaticViews, GET-only
app.add_url_rule('/about-us',
                 view_func=StaticView.as_view('about_us', template_name='about_us.html'))
app.add_url_rule('/contact-us',
                 view_func=StaticView.as_view('contact_us', template_name='contact_us.html'))
app.add_url_rule('/terms',
                 view_func=StaticView.as_view('terms', template_name='terms.html'))
app.add_url_rule('/privacy-policy',
                 view_func=StaticView.as_view('privacy_policy', template_name='privacy_policy.html'))
app.add_url_rule('/sitemap',
                 view_func=StaticView.as_view('sitemap', template_name='sitemap.xml'))
app.add_url_rule('/company/<string:company_profile_name>', # GET and POST
                 view_func=CompanyProfileView.as_view('company'))
app.add_url_rule('/my-account', # GET and POST
                 view_func=MyAccountView.as_view('my_account'))
app.add_url_rule('/forgot-password', # GET and POST
                 view_func=ForgotPasswordView.as_view('forgot_password'))
app.add_url_rule('/reset-password/<string:code>', # GET and POST
                 view_func=ResetPasswordView.as_view('reset_password'))
app.add_url_rule('/login', # GET and POST
                view_func=LoginView.as_view('login'))
app.add_url_rule('/signup', # GET and POST
                view_func=SignupView.as_view('signup'))
app.add_url_rule('/search-results',
                 view_func=SearchResultView.as_view('search_results'),
                 methods = ['POST'])
app.add_url_rule('/index',
                 view_func=IndexView.as_view('index'),
                 methods = ['GET'])
app.add_url_rule('/',
                 view_func=IndexView.as_view('/'),
                 methods = ['GET'])
app.add_url_rule('/verify-email/<string:code>',
                 view_func=VerifyEmailView.as_view('verify_email'),
                 methods = ['GET'])
app.add_url_rule('/LogoutView',
                 view_func=LogoutView.as_view('logout'),
                 methods = ['GET'])


minified = minified_files(static_path='static' ,local_path = 'app/static', mode=MODE)
app.jinja_env.globals['minified'] = minified
app.jinja_env.globals['sticky_note'] = add_sticky_note
app.jinja_env.globals['glossary'] = glossary

@app.before_request
def redirect_www():
    #http://stackoverflow.com/questions/9766134/how-do-i-redirect-to-the-www-version-of-my-flask-site-on-heroku
    """Redirect www requests to non-www"""
    urlparts = urlparse(request.url)
    urlparts_list = list(urlparts)
    if urlparts.netloc in {'www.52payments.com', 'www.localhost:8080'}:
        urlparts_list[1] = urlparts.netloc[4:]
        return redirect(urlunparse(urlparts_list), code=301)
    if urlparts.netloc.find('appspot')> 0:
        urlparts_list[1] = '52payments.com'
        return redirect(urlunparse(urlparts_list), code=301)

@app.errorhandler(401)
def page_not_found(e):
    flash("Requested page(%s) requires login OR you are not authorized. Redirected to main page. Thanks."%request.url)
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    flash("Requested page(%s) does not exist. Redirected to main page. Thanks."%request.url)
    return redirect(url_for('index'))

if MODE == 'local':
    @app.route('/add-companies', methods=['GET'])
    @login_required # only admin
    def add_companies():
        if current_user.email != 'admin@52payments.com' or not current_user.email_verified:
            abort(400)
        import_companies()
        return "####"
    @app.route('/temp', methods=['GET'])
    def temp():
        return render_template("temp.html")
#######################################################################
# Not being used. Need to work on below in order
# @app.route('/admin', methods=['GET', 'POST'])
# @login_required # only admin
# def admin():
#     logging.debug('###############')
#     if current_user.email != 'admin@52payments.com' or not current_user.email_verified:
#         abort(400)
#     logging.debug('###############')
#     reviews = ReviewModel.query().filter(ReviewModel.approved ==None).order(-ReviewModel.created).fetch(limit=None)
#     logging.debug('###############')
#     dict_reviews = []
#     logging.debug('###############')
#     for review in reviews:
#         urlsafe = review.key.urlsafe()
#         review = review.to_dict()
#         review['urlsafe'] = urlsafe
#         user = review['user'].get()
#         review['user_name'] = user.first_name + ' ' +user.last_name
#         dict_reviews.append(review)
#     logging.debug('###############')
#     return render_template('admin.html',
#                             reviews=dict_reviews)
#
# @app.route('/admindecision', methods=['POST'])
# @login_required # only admin
# def admindecision():
#     if current_user.email != 'admin@52payments.com' or not current_user.email_verified:
#         abort(400)
#     urlsafe = request.form['urlsafe']
#     key = ndb.Key(urlsafe = urlsafe)
#     obj_type = request.form['type']
#     decision = request.form['decision']
#     if obj_type == 'review':
#         review = key.get()
#         if decision == 'true':
#             k = review.approve()
#             return 'approved'
#         else:
#             review.key.delete()
#             return 'declined'
#
# @app.route('/register-company/<code>', methods=['GET', 'POST'])
# def register_company(code):
#     company_profile_name = TempCodeModel.verify_code(code, delete=False)
#     if not company_profile_name:
#         abort(400)
#     form = CompanyForm(company_profile_name=company_profile_name)
#     if form.validate_on_submit():
#         company_form = form.data
#         company_form['company_profile_name'] = company_form['company_profile_name'].lower()
#         if Company.load_company(company_form['company_profile_name']):
#             flash('The entered Url End Point is taken.')
#             return render_template('register_company.html', form = form)
#         company_form['logo_file'] = request.files['logo_file'].read()
#         for col in ['pricing', 'rate', 'per_transaction']:
#             company_form[col +'_range'] = [company_form[col + '_range_lower'],company_form[col + '_range_upper']]
#             company_form.pop(col + '_range_lower', None)
#             company_form.pop(col + '_range_upper', None)
#         if company_form.get('phones'):
#             company_form['phones'] = company_form['phones'].split(',')
#         if company_form.get('landing_page'):
#             if company_form['landing_page'].find('http://') == -1:
#                 company_form['landing_page'] = 'http://' + company_form['landing_page']
#         company = CompanyModel(**company_form)
#         company.put()
#         temp_code = TempCodeModel.load_code(code)
#         temp_code.key.delete()
#         flash('Info Submitted')
#         return redirect(url_for('company', company_profile_name = form.data['company_profile_name']))
#     return render_template('register_company.html', form = form)
