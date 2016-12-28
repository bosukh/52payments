import logging
import time
from time import sleep
from uuid import uuid1
from flask import Flask, make_response, abort, g, jsonify
from flask import render_template, flash, redirect, session, url_for, request, g
from google.appengine.ext import ndb
from google.appengine.api import memcache
from bcrypt import bcrypt as bt
from flask_login import fresh_login_required, LoginManager, login_user, logout_user, current_user, login_required
from app import app, login_manager
from app.forms import ChangePasswordForm, EditInfoForm, VerifyEmailForm, ForgotPasswordForm, GoogleLoginForm, CompanyForm, SearchForm, LoginForm, SignUpForm, ReviewForm, TestForm
from app.models import Company, User, Review
from app.momentjs import momentjs
from app.basejs import basejs
from app.search import parse_search_criteria, company_search
from app.memcache import mc_getsert
from app.login_manager import validate_user, load_user, google_oauth, login_user_with_redirect
from app.redirect_check import *
from app.emails import email_templates, send_email

app.jinja_env.globals['momentjs'] = momentjs
app.jinja_env.globals['bjs'] = basejs

def load_company(company_profile_name):
    query = Company.gql("WHERE company_profile_name = '%s'"%company_profile_name)
    return query.get()

@app.route('/search_results', methods=['GET'])
def search_results():
    if request.args['search_criteria']:
        search_criteria = parse_search_criteria(request.args['search_criteria'])
        search_result = company_search(search_criteria)
        for company in search_result:
            company.avg_rating = round(company.avg_rating, 1)
            session['search_criteria'] = search_criteria
    else:
        search_result = mc_getsert('all_verified_companies', Company.gql('').fetch)
    return render_template("search_results.html", companies=search_result)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('search_results'))
    #companies = Company.query(Company.featured==True).fetch(limit=3)
    companies = Company.query().fetch(limit=3)
    return render_template("index.html", companies = companies, form = form)

@app.route('/my_account', methods=['GET', 'POST'])
@login_required
def my_account():
    verify_email_form = VerifyEmailForm()
    edit_info_form = EditInfoForm()
    if edit_info_form.validate_on_submit():
        user_info = edit_info_form.data
        for k, v in user_info.iteritems():
            exec "current_user.%s = '%s'"%(k, str(v))
        current_user.put()
    if verify_email_form.validate_on_submit():
        if verify_email_form.data['verify_email'] != current_user.email:
            abort(400)
        code = uuid1().get_hex()
        memcache.add(code, current_user.user_id, time=time.time()+60*10)
        link = 'https://52payments.com/verify_email/%s'%code
        subject = email_templates['verify_email']['subject']
        body = email_templates['verify_email']['body']%(current_user.first_name, link)
        send_email(current_user, subject, body)
        flash('Email verification email is sent. Please check your email.')
        return redirect(url_for('my_account'))
    user = current_user.to_dict()
    user.pop('password')
    reviews = Review.query(Review.user==current_user.key).order(-Review.created).fetch(limit=None)
    reviews = [review.to_dict() for review in reviews]
    for review in reviews:
        review['user_name'] = user['first_name'] +' '+ user['last_name']
        company = review['company'].get()
        review['company_name'] = company.title
        review['company_profile_name'] = company.company_profile_name
    return render_template("my_account.html", user= user, reviews=reviews,
                           verify_email_form = verify_email_form, edit_info_form=edit_info_form)

@app.route('/verify_email/<code>', methods=['GET'])
def verify_email():
    user_id = memcache.get(code)
    if user_id:
        user = load_user(user)
        user.email_verified = True
        user.put()
        flash('Your email has been verified. Thank you')
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
            logging.debug(code)
            memcache.add(code, user.user_id, time=time.time()+60*10)
            link = 'https://52payments.com/reset_password/%s'%code
            subject = email_templates['forgot_password']['subject']
            body = email_templates['forgot_password']['body']%(user.first_name, link)
            send_email(user, subject, body)
            flash('Password re-set link is sent to your email. Please check your email.')
        return redirect(url_for('index'))
    return render_template('forgot_password.html', form=form)

@app.route('/reset_password/<code>', methods=['GET', 'POST'])
def reset_password(code):
    user_id = memcache.get(code)
    form = ChangePasswordForm()
    if user_id and not form.validate_on_submit():
        flash('Please change your password.')
        return render_template('change_password.html', form = form)
    elif user_id and form.validate_on_submit():
        user = load_user(user_id)
        user.password = bt.hashpw(form.data['password'], bt.gensalt())
        user.put()
        memcache.delete(code)
        flash('Your password is changed. Please login')
        return redirect(url_for('login'))
    else:
        flash('Your link is expired or incorrect. Please try again')
        return redirect(url_for('forgot_password'))

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
    return render_template('login.html', form=form, google_login_form= google_login_form)

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
        if user_data['password'] != user_data['password_2']:
            flash('Passwords have to match.')
            return render_template('signup.html', form=form)
        user = load_user(user_data['email'])
        if user:
            error = 'Your email is already registered.'
            flash(error)
            return render_template('signup.html', form=form)
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
    return render_template('signup.html', form=form, google_login_form= google_login_form)

@app.route('/register_company/<code>', methods=['GET', 'POST'])
def register_company(code):
    load_company(code)
    form = CompanyForm(company_profile_name='asd')
    if form.validate_on_submit():
        company_form = form.data
        company_form['company_profile_name'] = company_form['company_profile_name'].lower()
        if load_company(company_form['company_profile_name']):
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
        sleep(1)
        flash('Info Submitted')
        return redirect(url_for('company', company_profile_name = form.data['company_profile_name']))
    return render_template('register_company.html', form = form)

@app.route('/company/<company_profile_name>', methods = ['GET', 'POST'])
def company(company_profile_name):
    company = load_company(company_profile_name)
    form = ReviewForm()
    if form.validate_on_submit():
        if not current_user or not current_user.is_authenticated:
            flash('You need to log-in.')
        else:
            review = form.data
            review['rating'] = int(review['rating'])
            review['user'] = load_user(current_user.user_id).key
            review['company'] = load_company(company_profile_name).key
            review = Review(**review)
            review.put()
            flash('Your review is submitted. It should be up soon.')
            return redirect(url_for('company', company_profile_name = company_profile_name))
    if company:
        reviews = Review.query(Review.company==company.key).filter(Review.approved == True).order(-Review.created).fetch(limit=None)
        reviews = [review.to_dict() for review in reviews]
        for review in reviews:
            user = review['user'].get()
            review['user_name'] = user.first_name +" " + user.last_name
        return render_template('company_profile.html',
                                company = company, reviews = reviews, form=form)
    else:
        flash("Requested page does not exist. Redirected to the main page.")
        return redirect(url_for("index"))

@app.route('/admin', methods=['GET', 'POST'])
@login_required # only admin
def admin():
    reviews = Review.query().filter(Review.approved ==False).order(-Review.created).fetch(limit=None)
    dict_reviews = []
    for review in reviews:
        urlsafe = review.key.urlsafe()
        review = review.to_dict()
        review['urlsafe'] = urlsafe
        user = review['user'].get()
        review['user_name'] = user.first_name + ' ' +user.last_name
        dict_reviews.append(review)
    print dict_reviews
    return render_template('admin.html',
                            reviews=dict_reviews)

@app.route('/admindecision', methods=['POST'])
@login_required # only admin
def admindecision():
    urlsafe = request.form['urlsafe']
    key = ndb.Key(urlsafe = urlsafe)
    obj_type = request.form['type']
    decision = request.form['decision']
    if obj_type == 'review':
        review = key.get()
        if decision == 'true':
            review.approve()
            return 'approved'
        else:
            review.key.delete()
            return 'declined'

@app.route("/img/<company_profile_name>", methods=['GET'])
def img(company_profile_name):
    company = load_company(company_profile_name)
    company = company.logo_file
    response = make_response(company)
    response.headers['Content-Type'] = 'image/svg+xml'
    return response
###################################################
from random import choice
@app.route('/add_tests', methods=['GET', 'POST'])
def add_tests():
    def choose(list_, iter=5):
        temp = [choice(list_) for _ in range(iter)]
        temp = set(temp)
        return list(temp)

    summary = '''
                Lorem Ipsum is simply dummy text of the printing and
                typesetting industry. Lorem Ipsum has been the
                industry's standard dummy text ever since the 1500s,
                when an unknown printer took a galley of type and
                scrambled it to make a type specimen book. It has
                survived not only five centuries, but also the leap
                into electronic typesetting, remaining essentially
                unchanged. It was popularised in the 1960s with the
                release of Letraset sheets containing Lorem Ipsum
                passages, and more recently with desktop publishing
                software like Aldus PageMaker including versions of
                Lorem Ipsum.
                '''
    biz_type = ['Retail', 'Restaurant', 'E-Commerce', 'Healthcare/Medical', 'Mobile', 'Professional/Personal Services', 'Non-Profit', 'High-Risk', 'High-Volume', 'Other']
    srv_type = ['Marketing', 'Analytics', 'Recurling Bill', 'Chargeback', 'Security', 'Other']
    equip_type = ['Verifone', 'Ingenico', 'Other']
    pricing_type = ['Tiered', 'Interchange Plus', 'Flat', 'Custom']
    form = TestForm()
    if form.validate_on_submit():
        company_form = form.data
        company_form['logo_file'] = request.files['logo_file'].read()
        company = {}
        company.update(company_form)
        for i in range(1, 10):
            company['title'] = '52PAYMENTS_' + str(i)
            company['company_profile_name'] = '52payments_' + str(i)
            company['website'] = 'www.52payments.com'
            company['landing_page'] = 'http://www.52payments.com'
            company['phones'] = ['General: 000-0000-0000', 'Customer Service: 000-0000-0000']
            company['summary'] = summary
            company['full_description'] = summary*(i%4+1)
            company['year_founded'] = 2010+i%4
            company['provided_srvs'] = choose(biz_type)
            company['complementary_srvs'] = choose(srv_type)
            company['equipment'] = choose(equip_type)
            company['pricing_method'] = choose(pricing_type)
            company['pricing_range'] = [1, 1+i%5]
            company['rate_range'] = [1, 1+i%5]
            company['per_transaction_range'] = [0.1, 0.1+(i%5)*0.1]
            temp =Company(**company)
            temp.put()
        return redirect(url_for('index'))
    return render_template("add_tests.html", form = form)
