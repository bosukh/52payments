from . import render_template
from flask import flash, redirect, url_for, request
from flask.views import View, MethodView

from ..forms import SignUpForm, GoogleLoginForm
from ..login_manager import redirect_loggedin_user, NormalAuth, GoogleOauth
from flask_login import current_user, login_required

class SignupView(View):
    methods = ['GET', 'POST']
    decorators = [redirect_loggedin_user('my_account')]
    def dispatch_request(self):
        form = SignUpForm()
        google_login_form =GoogleLoginForm()
        if request.method == 'POST' and form.validate_on_submit() or google_login_form.validate_on_submit():
            if form.validate_on_submit():
                auth = NormalAuth(form)
            else:
                auth = GoogleOauth(google_login_form.data.get('id_token', ''))
            user = auth.signup()
            if user and not auth.error:
                return redirect(auth.redirect or url_for('index'))
            flash(auth.error or "Please try again")
        return render_template('signup.html', form=form, google_login_form= google_login_form,
                               title = 'Signup')
