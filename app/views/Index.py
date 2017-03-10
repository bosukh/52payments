from . import render_template

from flask.views import MethodView

from ..forms import SearchForm
from ..memcache import mc_getsert
from ..models import Company

class IndexView(MethodView):
    def get(self):
        form = SearchForm()
        companies =  mc_getsert('featured_companies', Company.make_query("WHERE featured=True ORDER BY share DESC LIMIT 3"))
        return render_template("index.html", companies = companies, form = form,
                               title='Search and Compare Card Payment Processors | 52Payments',
                               keywords= 'card processing, card processor, merchant accounts, payment processing solutions, Credit Card Processing Services',
                               description = 'Explore the options in accepting card payments for your business. Come find the most cost-effective card payment processors with our reviews.')
