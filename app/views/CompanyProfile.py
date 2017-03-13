from . import render_template

import logging
from flask import flash, redirect, url_for, request
from flask.views import View
from flask_login import current_user
from uuid import uuid1

from ..emails import email_templates, send_email
from ..forms.WriteReview import NonMemberWriteReviewForm, MemberWriteReviewForm
from ..models.Company import CompanyModel
from ..models.Review import ReviewModel
from ..models.User import UserModel
from ..login_manager import load_user


class CompanyProfileView(View):
    methods = ['GET', 'POST']
    def dispatch_request(self, company_profile_name):
        if current_user and current_user.is_authenticated:
            form = MemberWriteReviewForm()
        else:
            form = NonMemberWriteReviewForm()
        company = CompanyModel.load_company(company_profile_name)
        if not company:
            flash("Requested page does not exist. Redirected to the main page.")
            return redirect(url_for("index"))
        if request.method == 'POST' and form.validate_on_submit():
            review = form.data
            if current_user and current_user.is_authenticated:
                user = current_user #load_user(current_user.user_id).key
            else:
                temp_user_id = review['first_name'] + review['last_name'] + review['email']
                user = load_user(temp_user_id)
                if not user:
                    user = UserModel(first_name = review['first_name'],
                                     last_name = review['last_name'],
                                     email = review['email'],
                                     user_id = temp_user_id)
                    user.put()
            review = ReviewModel(rating = int(review['rating']),
                                 title = review['title'],
                                 content = review['content'],
                                 company = CompanyModel.load_company(company_profile_name).key,
                                 user = user.key)
            review.put()
            flash('Your review is submitted. It should be up soon.')
        reviews = ReviewModel.query(ReviewModel.company==company.key).filter(ReviewModel.approved == True).order(-ReviewModel.created).fetch(limit=None)
        reviews = ReviewModel.reviews_for_display(reviews)
        return render_template('company_profile.html',
                                company = company, reviews = reviews, form=form,
                                title = '%s Review | 52payments'%company.title.strip(),
                                keywords = "%s, search and compare payment processors, merchant account, card processor, payment processor"%company.title,
                                description = company.meta_description.strip())
