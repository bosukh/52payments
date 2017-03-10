from . import render_template

from flask import request
from flask.views import MethodView

from ..search import search_company

class SearchResultView(MethodView):
    def post(self):
        search_result = search_company(request.form['search_criteria'])
        return render_template("search_results.html", companies=search_result)
