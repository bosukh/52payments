from . import render_template

import logging
from flask import flash, redirect, url_for, request, abort
from flask.views import View
from flask_login import current_user, login_required

from ..emails import email_templates, send_email
from ..forms import VerifyEmailForm, EditInfoForm
from ..models import Review, TempCode

class MyAccountView(View):
    methods = ['GET', 'POST']
    decorators = [login_required]
    def dispatch_request(self):
        verify_email_form = VerifyEmailForm()
        edit_info_form = EditInfoForm()
        if request.method == 'POST':
            if edit_info_form.validate_on_submit():
                user_info = edit_info_form.data
                if current_user.email.lower().strip() != user_info.get('email').lower().strip():
                    current_user.email_verified = False
                for k, v in user_info.iteritems():
                    exec "current_user.%s = '%s'"%(k, str(v))
                current_user.put()
            elif verify_email_form.validate_on_submit():
                if verify_email_form.data['verify_email'] != current_user.email:
                    abort(400)
                subject = email_templates['verify_email']['subject']
                body = email_templates['verify_email']['body']%(current_user.first_name, 'https://52payments.com/verify-email/%s'%str(TempCode.gen_code()))
                send_email(current_user, subject, body)
                flash('Email verification link is sent. Please check your email.')
        user = current_user.to_dict()
        user.pop('password', None)
        reviews = Review.query(Review.user == current_user.key and Review.approved == True).order(-Review.created).fetch(limit = None)
        reviews = Review.reviews_for_display(reviews)
        for review in reviews:
            company = review['company'].get()
            review['company_name'] = company.title
            review['company_profile_name'] = company.company_profile_name
        return render_template("my_account.html", user = user, reviews = reviews,
                               verify_email_form = verify_email_form, edit_info_form = edit_info_form,
                               title = 'My Account | 52payments')
