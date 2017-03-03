import logging
from time import sleep
from uuid import uuid1
from flask import Flask, make_response, abort, g, jsonify
from flask import render_template as flask_render_template
from flask import flash, redirect, session, url_for, request
from rjscssmin_plugin import minified_files, html_minify
from google.appengine.ext import ndb
from google.appengine.api import memcache
from bcrypt import bcrypt as bt
from flask_login import fresh_login_required, LoginManager, login_user, logout_user, current_user, login_required

from app import app, login_manager
from app.forms import ChangePasswordForm, EditInfoForm, VerifyEmailForm, ForgotPasswordForm, GoogleLoginForm, CompanyForm, SearchForm, LoginForm, SignUpForm, ReviewForm
from app.models import Company, User, Review, TempCode
from app.basejs import basejs
from app.search import search_company
from app.memcache import mc_getsert
from app.login_manager import validate_user, load_user, google_oauth, login_user_with_redirect, load_user_by_email
from app.redirect_check import *
from app.emails import email_templates, send_email
from app.glossary import glossary
from app.sticky_notes import add_sticky_note, add_notes
from app.import_companies import import_companies
from config import MODE
from urlparse import urlparse, urlunparse

def render_template(*args, **kwargs):
    res = flask_render_template(*args, **kwargs)
    return html_minify(res)

minified = minified_files(static_path='static' ,local_path = 'app/static', mode=MODE)
app.jinja_env.globals['bjs'] = basejs
app.jinja_env.globals['minified'] = minified
app.jinja_env.globals['sticky_note'] = add_sticky_note
app.jinja_env.globals['glossary'] = glossary

if MODE == 'local':
    @app.route('/add_companies', methods=['GET'])
    @login_required # only admin
    def add_companies():
        if current_user.email != 'benbosukhong@gmail.com' or not current_user.email_verified:
            abort(400)
        import_companies()
        return "Success?"
    @app.route('/temp', methods=['GET'])
    def temp():
        return render_template("temp.html")

@app.errorhandler(404)
def page_not_found(e):
    flash("Requested page(%s) does not exist. Redirected to main page. Thanks."%request.url)
    return redirect(url_for('index'))

@app.before_request
def redirect_www():
    #http://stackoverflow.com/questions/9766134/how-do-i-redirect-to-the-www-version-of-my-flask-site-on-heroku
    """Redirect www requests to non-www"""
    urlparts = urlparse(request.url)
    urlparts_list = list(urlparts)
    if urlparts.netloc in {'www.52payments.com', 'www.localhost:8080'}:
        urlparts_list[1] = urlparts.netloc[:4]
        logging.debug(urlunparse(urlparts_list))
        return redirect(urlunparse(urlparts_list), code=301)
    if urlparts.netloc.find('appspot')> 0:
        urlparts_list[1] = '52payments.com'
        logging.debug(urlunparse(urlparts_list))
        return redirect(urlunparse(urlparts_list), code=301)

@app.route('/sitemap', methods=['GET'])
def sitemap():
    return render_template("sitemap.xml")

@app.route('/about_us', methods=['GET'])
def about_us():
    return render_template("about_us.html")
@app.route('/contact_us', methods=['GET'])
def contact_us():
    return render_template("contact_us.html")
@app.route('/terms', methods=['GET'])
def terms():
    return render_template("terms.html")
@app.route('/privacy_policy', methods=['GET'])
def privacy_policy():
    return render_template("privacy_policy.html")

@app.route('/search_results', methods=['POST'])
def search_results():
    search_result = search_company(request.form['search_criteria'])
    return render_template("search_results.html", companies=add_notes(search_result))

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('search_results'))
    #companies = Company.query(Company.featured==True).fetch(limit=3)
    #companies = Company.gql("ORDER BY share DESC LIMIT 3").fetch()
    companies = Company.gql("WHERE featured=True ORDER BY share DESC LIMIT 3").fetch()
    for company in companies:
        company.avg_rating = round(company.avg_rating, 1)
    return render_template("index.html", companies = add_notes(companies), form = form,
                           title='Search and Compare Card Payment Processors | 52Payments',
                           keywords= 'card processing, card processor, merchant accounts, payment processing solutions, Credit Card Processing Services',
                           description = 'Explore the options in accepting card payments for your business. Come find the most cost-effective card payment processors with our reviews.')

@app.route('/my_account', methods=['GET', 'POST'])
@login_required
def my_account():
    verify_email_form = VerifyEmailForm()
    edit_info_form = EditInfoForm()
    if edit_info_form.validate_on_submit():
        user_info = edit_info_form.data
        #validate {'email': u'benbosukhong@gmail.com', 'first_name': u'BosukSASDMK', 'company_name': u'sadfasdf', 'last_name': u'Hong', 'phone': u'3128751254'}
        for k, v in user_info.iteritems():
            exec "current_user.%s = '%s'"%(k, str(v))
        current_user.put()
    if verify_email_form.validate_on_submit():
        if verify_email_form.data['verify_email'] != current_user.email:
            abort(400)
        code = uuid1().get_hex()
        temp_code = TempCode(code=code, value=current_user.user_id)
        temp_code.put()
        link = 'https://52payments.com/verify_email/%s'%str(code)
        subject = email_templates['verify_email']['subject']
        body = email_templates['verify_email']['body']%(current_user.first_name, link)
        send_email(current_user, subject, body)
        flash('Email verification email is sent. Please check your email.')
        return redirect(url_for('my_account'))
    user = current_user.to_dict()
    user.pop('password')
    reviews = Review.query(Review.user==current_user.key).order(-Review.created).fetch(limit=None)
    reviews = Review.reviews_for_display(reviews)
    for review in reviews:
        company = review['company'].get()
        review['company_name'] = company.title
        review['company_profile_name'] = company.company_profile_name
    return render_template("my_account.html", user= user, reviews=reviews,
                           verify_email_form = verify_email_form, edit_info_form=edit_info_form,
                           title = 'My Account')

@app.route('/verify_email/<code>', methods=['GET'])
def verify_email(code):
    value = TempCode.verify_code(code, 600)
    if value:
        user = load_user(value)
        user.email_verified = True
        user.put()
        flash('Your email is now verified. Thank you')
    else:
        flash('Your email verification link is expired. Please try again.')
    return redirect(url_for('index'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    def check_user():
        user = load_user(form.data['email'])
        if not user:
            flash('Your email is not registered. Please sign up.')
            return False
        else:
            if user.first_name.lower() != form.data['first_name'].lower() or user.last_name.lower() != form.data['last_name'].lower():
                flash('Entered name does not match the email.')
                return False
        return user
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = check_user()
        if user:
            code = uuid1().get_hex()
            temp_code = TempCode(code=code, value=user.user_id)
            temp_code.put()
            link = 'https://52payments.com/reset_password/%s'%code
            subject = email_templates['forgot_password']['subject']
            body = email_templates['forgot_password']['body']%(user.first_name, link)
            send_email(user, subject, body)
            flash('Password re-set link is sent to your email. Please check your email.')
            return redirect(url_for('index'))
    return render_template('forgot_password.html', form=form)

@app.route('/reset_password/<code>', methods=['GET', 'POST'])
def reset_password(code):
    user_id = TempCode.verify_code(code, 600, delete=False)
    form = ChangePasswordForm()
    if user_id and not form.validate_on_submit():
        flash('Please change your password.')
        return render_template('change_password.html', form = form)
    elif user_id and form.validate_on_submit():
        temp_code = TempCode.load_code(code)
        temp_code.key.delete()
        user = load_user(user_id)
        user.password = bt.hashpw(form.data['password'], bt.gensalt())
        user.put()
        flash('Your password is changed. Please login')
        return redirect(url_for('login'))
    else:
        flash('Your link is expired or incorrect. Please try again')
        return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.referrer and request.referrer.find('login')==-1:
        session['initial_referrer'] = request.referrer
    form = LoginForm()
    google_login_form =GoogleLoginForm()
    if form.validate_on_submit():
        user, error = validate_user(form)
        if error:
            flash(error)
            return render_template('login.html', form=form, google_login_form= google_login_form)
        else:
            current_user, redirect_route = login_user_with_redirect(user, form, session.get('initial_referrer'))
            if current_user:
                return redirect(redirect_route or url_for('index'))
            else:
                return abort(400)
    if google_login_form.validate_on_submit():
        args = {}
        args['id_token'] = google_login_form.data['id_token']
        args['request_type'] = 'login'
        user, error = google_oauth(**args)
        if error:
            flash(error)
            return render_template('login.html', form=form, google_login_form= google_login_form)
        current_user, redirect_route = login_user_with_redirect(user, google_login_form, session.get('initial_referrer'))
        if current_user:
            return redirect(redirect_route or url_for('index'))
        else:
            return abort(400)
    return render_template('login.html', form=form, google_login_form= google_login_form,
                           title = 'Login')


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    logging.debug(request.referrer)
    referrer = request.referrer
    if not check_referrer_origin(referrer) or check_referrer_auth_requirement(referrer):
        referrer = None;
    flash('Logged out successfully. Thanks.')
    return redirect(referrer or url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    google_login_form =GoogleLoginForm()
    if form.validate_on_submit():
        user_data = form.data
        user = load_user(user_data['email'])
        if user:
            error = 'Your email is already registered.'
            flash(error)
            return render_template('signup.html', form=form, google_login_form= google_login_form)
        elif not user:
            user_data['password'] = bt.hashpw(user_data['password'], bt.gensalt())
            user_data.pop('password_2')
            user_data['user_id'] = user_data['email']
            user = User(**user_data)
            user.put()
        flash('Successfully registered. Please login.')
        return redirect(url_for('login'))
    if google_login_form.validate_on_submit():
        args = {}
        args['id_token'] = google_login_form.data['id_token']
        args['request_type'] = 'signup'
        user, error = google_oauth(**args)
        if error:
            flash(error)
            return render_template('signup.html', form=form, google_login_form= google_login_form)
        flash('Successfully registered. Please login.')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form, google_login_form= google_login_form,
                           title = 'Signup')


@app.route('/register_company/<code>', methods=['GET', 'POST'])
def register_company(code):
    company_profile_name = TempCode.verify_code(code, delete=False)
    if not company_profile_name:
        abort(400)
    form = CompanyForm(company_profile_name=company_profile_name)
    if form.validate_on_submit():
        company_form = form.data
        company_form['company_profile_name'] = company_form['company_profile_name'].lower()
        if Company.load_company(company_form['company_profile_name']):
            flash('The entered Url End Point is taken.')
            return render_template('register_company.html', form = form)
        company_form['logo_file'] = request.files['logo_file'].read()
        for col in ['pricing', 'rate', 'per_transaction']:
            company_form[col +'_range'] = [company_form[col + '_range_lower'],company_form[col + '_range_upper']]
            company_form.pop(col + '_range_lower', None)
            company_form.pop(col + '_range_upper', None)
        if company_form.get('phones'):
            company_form['phones'] = company_form['phones'].split(',')
        if company_form.get('landing_page'):
            if company_form['landing_page'].find('http://') == -1:
                company_form['landing_page'] = 'http://' + company_form['landing_page']
        company = Company(**company_form)
        company.put()
        temp_code = TempCode.load_code(code)
        temp_code.key.delete()
        sleep(1)
        flash('Info Submitted')
        return redirect(url_for('company', company_profile_name = form.data['company_profile_name']))
    return render_template('register_company.html', form = form)

@app.route('/company/<company_profile_name>', methods = ['GET', 'POST'])
def company(company_profile_name):
    company = Company.load_company(company_profile_name)
    form = ReviewForm()
    if form.validate_on_submit():
        if not current_user or not current_user.is_authenticated:
            flash('You need to log-in.')
        else:
            review = form.data
            review['rating'] = int(review['rating'])
            review['user'] = load_user(current_user.user_id).key
            review['company'] = Company.load_company(company_profile_name).key
            review = Review(**review)
            review.put()
            flash('Your review is submitted. It should be up soon.')
            return redirect(url_for('company', company_profile_name = company_profile_name))
    if company:
        reviews = Review.query(Review.company==company.key).filter(Review.approved == True).order(-Review.created).fetch(limit=None)
        reviews = Review.reviews_for_display(reviews)
        company.avg_rating = round(company.avg_rating, 1)
        return render_template('company_profile.html',
                                company = add_notes(company), reviews = reviews, form=form,
                                title = '%s Review'%company.title.strip(),
                                keywords = "%s, search and compare payment processors, merchant account, card processor, payment processor"%company.title,
                                description = company.meta_description.strip())
    else:
        flash("Requested page does not exist. Redirected to the main page.")
        return redirect(url_for("index"))

@app.route('/admin', methods=['GET', 'POST'])
@login_required # only admin
def admin():
    if current_user.email != 'benbosukhong@gmail.com' or not current_user.email_verified:
        abort(400)
    reviews = Review.query().filter(Review.approved ==None).order(-Review.created).fetch(limit=None)
    dict_reviews = []
    for review in reviews:
        urlsafe = review.key.urlsafe()
        review = review.to_dict()
        review['urlsafe'] = urlsafe
        user = review['user'].get()
        review['user_name'] = user.first_name + ' ' +user.last_name
        dict_reviews.append(review)
    return render_template('admin.html',
                            reviews=dict_reviews)

@app.route('/admindecision', methods=['POST'])
@login_required # only admin
def admindecision():
    if current_user.email != 'benbosukhong@gmail.com' or not current_user.email_verified:
        abort(400)
    urlsafe = request.form['urlsafe']
    key = ndb.Key(urlsafe = urlsafe)
    obj_type = request.form['type']
    decision = request.form['decision']
    if obj_type == 'review':
        review = key.get()
        if decision == 'true':
            k = review.approve()
            return 'approved'
        else:
            review.key.delete()
            return 'declined'
