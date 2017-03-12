from . import Form

from wtforms import HiddenField

class SearchCompanyForm(Form):
    search_criteria = HiddenField('search_criteria')
