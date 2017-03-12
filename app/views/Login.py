from . import render_template

from flask import flash, redirect, url_for, request, session
from flask.views import View

from ..forms.Login import LoginForm
from ..forms.GoogleLogin import GoogleLoginForm
from ..login_manager import redirect_loggedin_user, GoogleOauth, NormalAuth

class LoginView(View):
    methods = ['GET', 'POST']
    decorators = [redirect_loggedin_user('my_account')]
    def dispatch_request(self):
        if request.referrer and request.referrer.find('login')==-1:
            session['initial_referrer'] = request.referrer
        form = LoginForm()
        google_login_form = GoogleLoginForm()
        if request.method == 'POST' and form.validate_on_submit() or google_login_form.validate_on_submit():
            if form.validate_on_submit():
                auth = NormalAuth(form)
            else:
                auth = GoogleOauth(google_login_form.data.get('id_token', ''))
            user = auth.login()
            if user and not auth.error:
                return redirect(auth.redirect or url_for('index'))
            flash(auth.error or "Please try again")
        return render_template('login.html', form=form, google_login_form= google_login_form,
                               title = 'Login')
