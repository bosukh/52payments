import logging

from flask import flash, redirect, url_for, request
from flask.views import MethodView
from flask_login import logout_user

from ..forms import LoginForm, GoogleLoginForm
from ..login_manager import redirect_loggedin_user, GoogleOauth, NormalAuth
from ..redirect_check import check_referrer_auth_requirement, check_referrer_origin

class LogoutView(MethodView):
    def get(self):
        logout_user()
        logging.debug(request.referrer)
        referrer = request.referrer
        if not check_referrer_origin(referrer) or check_referrer_auth_requirement(referrer):
            referrer = None;
        flash('Logged out successfully. Thanks.')
        return redirect(referrer or url_for('index'))
