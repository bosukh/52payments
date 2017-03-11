from flask import flash, redirect, url_for
from flask.views import MethodView

from ..login_manager import load_user
from ..models.TempCode import TempCodeModel

class VerifyEmailView(MethodView):
    def get(self, code):
        value = TempCodeModel.verify_code(code, 600)
        if value:
            user = load_user(value)
            user.email_verified = True
            user.put()
            flash('Your email is now verified. Thank you')
        else:
            flash('Your email verification link is expired. Please try again.')
        return redirect(url_for('index'))
