import os

from flask import Flask, make_response, abort
from flask import render_template, flash, redirect, session, url_for, request, g
from config import basedir
from google.appengine.ext import db
from bcrypt import bcrypt as bt
from flask_login import LoginManager, login_user, logout_user, current_user, login_required


app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager()
login_manager.init_app(app)

from app.forms import CompanyForm, SearchForm, LoginForm, SignUpForm
from app.models import Company, User, Review

@login_manager.user_loader
def load_user(email):
    query = User.gql("WHERE email = '%s'"%email)
    return query.get()

def load_company(company_profile_name):
    query = Company.gql("WHERE company_profile_name = '%s'"%company_profile_name)
    company = query.get()
    return company

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        user = load_user(form.data['email'])
        try:
            input_pw = bt.hashpw(form.data['password'], user.password)
            if input_pw == user.password:
                user.authenticated = True
                login_user(user)
                current_user = user
                flash('Logged in successfully.')
                #next = request.args.get('next')
                #if not next:
                #    return abort(400)
                #return redirect(next or flask.url_for('index'))
                return redirect(url_for('index'))
        except ValueError:
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user_data = form.data
        existing = load_user(user_data['email'])
        if existing:
            flash('Your email is already registered.')
            return redirect('login')
        user_data['password'] = bt.hashpw(user_data['password'], bt.gensalt())
        user_data.pop('password_2')
        user = User(**user_data)
        user.put()
        flash('Signup successful')
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)

def test_db():
    ben = User(first_name = 'Ben', last_name = 'Hong',email= 'ben@test.com', password = 'benpw')
    ben.put()
    sarah = User(first_name = 'Sarah', last_name = 'Bang', email= 'sarah@test.com', password = 'sarahpw')
    sarah.put()
    query = Company.gql("WHERE company_profile_name = '%s'"%'52payments')
    ft_payments = query.get()
    ben_review = Review(rating = 5.0, title = 'first review',
                        content = '52 payments is now starting',
                        user = ben, company = ft_payments)
    ben_review.put_review()
    sarah_review = Review(rating = 5.0, title = 'second review',
                        content = '52 payments can be big!',
                        user = sarah, company = ft_payments)
    sarah_review.put_review()

#test_db()
@app.route('/register_company', methods=['GET', 'POST'])
@login_required
def register_company():
    form = CompanyForm()
    if form.validate_on_submit():
        company_form = form.data
        company_form['logo_file'] = request.files['logo_file'].read()
        company = Company(**company_form)
        company.put()
        flash('Info Submitted')
        return redirect(url_for('index'))
    else:
        flash('Information Not Valid')
    return render_template('register_company.html', form = form)

@app.route('/register_user', methods=['GET', 'POST'])
def register_user():
    return '<h1>register_user</h1>'

@app.route('/company_write_review/<company_profile_name>')
def company_write_review(company_profile_name):
    return '<h1>Write a review for %s</h1>'%company_profile_name


@app.route('/company/<company_profile_name>')
def company(company_profile_name):
    company = load_company(company_profile_name)
    if company:
        return render_template('company_profile.html',
                                company = company)
    else:
        flash("Requested page does not exist. Redirected to the main page.")
        return redirect(url_for("index"))

@app.route('/search_results')
def search_results():
    temp = ''
    for k, v in session['search_form'].iteritems():
        temp+=k
    return temp

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        session['search_form'] = form.data
        return redirect(url_for('search_results'))
    query = db.Query(Company)
    companies = query.fetch(limit=3)
    return render_template('index.html',
                            form=form,
                            companies = companies)

@app.route("/img/<company_profile_name>")
def img(company_profile_name):
    company = load_company(company_profile_name)
    company = company.logo_file
    response = make_response(company)
    response.headers['Content-Type'] = 'image/svg+xml'
    return response
