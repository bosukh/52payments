import time

from flask import Flask, make_response, abort, g
from flask import render_template, flash, redirect, session, url_for, request, g
from config import basedir
from google.appengine.ext import ndb
from google.appengine.api import memcache
from bcrypt import bcrypt as bt
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from app import app, login_manager
from app.forms import CompanyForm, SearchForm, LoginForm, SignUpForm, ReviewForm
from app.models import Company, User, Review
from app.momentjs import momentjs
from app.basejs import basejs
from app.search import parse_search_criteria, company_search
from app.memcache import mc_getsert
from app.login_manager import load_user, google_oauth_singin, google_oauth_signup
app.jinja_env.globals['momentjs'] = momentjs
app.jinja_env.globals['bjs'] = basejs

@app.route('/search_results', methods=['GET'])
def search_results():
    if request.args['search_criteria']:
        search_criteria = parse_search_criteria(request.args['search_criteria'])
        search_result = company_search(search_criteria)
        session['search_criteria'] = search_criteria
        print search_criteria
    else:
        search_result = mc_getsert('all_verified_companies', Company.gql('WHERE verified = True').fetch)
    return render_template("search_results.html", companies=search_result)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('search_results'))
    companies = Company.query().fetch(limit=3)
    return render_template("index.html", companies = companies, form = form)

def load_company(company_profile_name):
    query = Company.gql("WHERE company_profile_name = '%s'"%company_profile_name)
    return query.get()


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.data['id_token']:
            user, error = google_oauth_singin(**form.data)
        elif form.data['email'] and form.data['password']:
            user = load_user(form.data['email'])
            if not user:
                error  = 'The given email is not registered'
            else:
                try:
                    input_pw = bt.hashpw(form.data['password'], user.password)
                    if input_pw == user.password:
                        user.authenticated = True
                except ValueError:
                    error = 'The given password is not correct'
        else:
            error = 'You must enter both email and password'
        if error:
            flash(error)
            return render_template('login.html', form=form)
        else:
            if form.redirect():
                login_user(user)
                current_user = user
                flash('Logged in successfully.')
                return redirect(url_for('index'))
            else:
                return abort(400)
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user_data = form.data
        if user_data['id_token']:
            user, error = google_oauth_signup(**user_data)
        elif user_data['email']:
            user = load_user(user_data['email'])
            error = 'Your email is already registered.'
        if error:
            flash(error)
            return render_template('signup.html', form=form)
        elif not user:
            user_data['password'] = bt.hashpw(user_data['password'], bt.gensalt())
            user_data.pop('password_2')
            user_data.pop('id_token')
            user_data['user_id'] = user_data['email']
            user = User(**user_data)
            user.put()
        flash('Signup successful')
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)

@app.route('/register_company', methods=['GET', 'POST'])
@login_required # make it accessible only by business account
def register_company():
    form = CompanyForm()
    if form.validate_on_submit():
        company_form = form.data
        company_form['logo_file'] = request.files['logo_file'].read()
        company_form['pricing_range'] = [company_form['pricing_range_lower'],company_form['pricing_range_upper']]
        company_form.pop('pricing_range_lower', None)
        company_form.pop('pricing_range_upper', None)
        company = Company(**company_form)
        company.put()
        time.sleep(1)
        flash('Info Submitted')
        return redirect(url_for('company', company_profile_name = form.data['company_profile_name']))
    return render_template('register_company.html', form = form)

@app.route('/company_write_review/<company_profile_name>', methods=['GET', 'POST'])
@login_required # Make it accessible only by customer account
def company_write_review(company_profile_name):
    form = ReviewForm()
    if form.validate_on_submit():
        review = form.data
        review['rating'] = int(review['rating'])
        review['user'] = load_user(current_user.email).key
        review['company'] = load_company(company_profile_name).key
        review = Review(**review)
        review.put()
        flash('Your review is submitted.')
        time.sleep(1)
        return redirect(url_for('company', company_profile_name = company_profile_name))
    return render_template('write_review.html', form=form)

@app.route('/company/<company_profile_name>')
def company(company_profile_name):
    company = load_company(company_profile_name)
    if company:
        reviews = Review.query(Review.company==company.key).filter(Review.approved == True).order(-Review.created).fetch(limit=None)
        reviews = [review.to_dict() for review in reviews]
        for review in reviews:
            user = review['user'].get()
            review['user_name'] = user.first_name +" " + user.last_name
        return render_template('company_profile.html',
                                company = company, reviews = reviews)
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
            review.delete()
            return 'declined'

@app.route("/img/<company_profile_name>")
def img(company_profile_name):
    company = load_company(company_profile_name)
    company = company.logo_file
    response = make_response(company)
    response.headers['Content-Type'] = 'image/svg+xml'
    return response
