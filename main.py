import os

from flask import Flask, make_response
from flask import render_template, flash, redirect, session, url_for, request, g
from config import basedir
from google.appengine.ext import db
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
app = Flask(__name__)
app.config.from_object('config')

from app.forms import CompanyForm, SearchForm
from app.models import Company, User, Review

@app.route('/temp', methods=['GET', 'POST'])
def temp():
    test_db()
    a = ''
    query = Company.gql("WHERE company_profile_name = '%s'"%'52payments')
    company = query.get()
    return a + ' ' + str(company.review_set.count())


def test_db():
    ben = User(name = 'Ben')
    ben.put()
    sarah = User(name = 'Sarah')
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

#fill_db()
@app.route('/register_company', methods=['GET', 'POST'])
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
    query = Company.gql("WHERE company_profile_name = '%s'"%company_profile_name)
    company = query.get()
    return render_template('company_profile.html',
                            company = company)

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
    query = Company.gql("WHERE company_profile_name = '%s'"%company_profile_name)
    a= query.get()
    a = a.logo_file
    response = make_response(a)
    response.headers['Content-Type'] = 'image/svg+xml'
    return response
