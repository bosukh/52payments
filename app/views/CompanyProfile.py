from . import render_template

import logging
from flask import flash, redirect, url_for, request
from flask.views import View
from flask_login import current_user

from ..emails import email_templates, send_email
from ..forms import ReviewForm
from ..models import Company, Review


class CompanyProfileView(View):
    methods = ['GET', 'POST']
    def dispatch_request(self, company_profile_name):
        form = ReviewForm()
        company = Company.load_company(company_profile_name)
        if not company:
            flash("Requested page does not exist. Redirected to the main page.")
            return redirect(url_for("index"))
        if request.method == 'POST' and form.validate_on_submit():
            if not current_user or not current_user.is_authenticated:
                flash('You need to log-in.')
            else:
                review = form.data
                review['rating'] = int(review['rating'])
                review['user'] = current_user.key #load_user(current_user.user_id).key
                review['company'] = Company.load_company(company_profile_name).key
                review = Review(**review)
                review.put()
                flash('Your review is submitted. It should be up soon.')
        reviews = Review.query(Review.company==company.key).filter(Review.approved == True).order(-Review.created).fetch(limit=None)
        reviews = Review.reviews_for_display(reviews)
        return render_template('company_profile.html',
                                company = company, reviews = reviews, form=form,
                                title = '%s Review | 52payments'%company.title.strip(),
                                keywords = "%s, search and compare payment processors, merchant account, card processor, payment processor"%company.title,
                                description = company.meta_description.strip())
