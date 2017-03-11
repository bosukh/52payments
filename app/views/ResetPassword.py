from . import render_template

from bcrypt import bcrypt as bt
from flask import flash, redirect, url_for, request
from flask.views import View

from ..login_manager import load_user
from ..forms import ChangePasswordForm
from ..models.TempCode import TempCodeModel

class ResetPasswordView(View):
    methods = ['GET', 'POST']
    def dispatch_request(self, code):
        user_id = TempCodeModel.verify_code(code, 600, delete=False)
        form = ChangePasswordForm()
        if not user_id:
            flash('Your link is expired or incorrect. Please try again')
            return redirect(url_for('index'))
        if request.method == 'POST' and form.validate_on_submit():
            temp_code = TempCodeModel.load_code(code)
            temp_code.key.delete()
            user = load_user(user_id)
            user.password = bt.hashpw(form.data['password'], bt.gensalt())
            user.put()
            flash('Your password is changed. Please login')
            return redirect(url_for('login'))
        flash('Please change your password.')
        return render_template('change_password.html', form = form)
