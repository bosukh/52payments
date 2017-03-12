from flask import url_for
from flask_wtf import FlaskForm
from wtforms import HiddenField

from ..redirect_check import is_safe_url, get_redirect_target

class Form(FlaskForm):
    @property
    def data(self):
        res = dict((name, f.data) for name, f in self._fields.iteritems())
        res.pop('csrf_token', None)
        return res

class RedirectForm(Form):
    next = HiddenField()
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self):
        target = get_redirect_target()
        if target and is_safe_url(target):
            return target
        else:
            return url_for('index') #redirect(self.next.data)
