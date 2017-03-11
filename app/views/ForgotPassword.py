from . import render_template

import logging
from flask import flash, redirect, url_for, request
from flask.views import View

from ..emails import email_templates, send_email
from ..login_manager import load_user
from ..forms import ForgotPasswordForm
from ..models.TempCode import TempCodeModel

class ForgotPasswordView(View):
    methods = ['GET', 'POST']
    def dispatch_request(self):
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
        if request.method == 'POST' and form.validate_on_submit():
            user = check_user()
            if user:
                subject = email_templates['forgot_password']['subject']
                body = email_templates['forgot_password']['body']%(user.first_name, 'https://52payments.com/reset-password/%s'%str(TempCodeModel.gen_code(user.user_id)))
                logging.debug(subject)
                logging.debug(body)
                send_email(user, subject, body)
                flash('Password re-set link is sent to your email. Please check your email.')
                return redirect(url_for('index'))
        return render_template('forgot_password.html', form=form) #GET
