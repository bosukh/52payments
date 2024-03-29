from . import render_template

from flask.views import MethodView

from ..forms.SearchCompany import SearchCompanyForm
from ..memcache import mc_getsert
from ..models.Company import CompanyModel

class IndexView(MethodView):
    def get(self):
        form = SearchCompanyForm()
        companies =  mc_getsert('featured_companies', CompanyModel.make_query("WHERE featured=True ORDER BY share DESC LIMIT 3"))
        return render_template("index.html", companies = companies, form = form,
                               title='Search and Compare Card Payment Processors | 52Payments',
                               keywords= 'card processing, card processor, merchant accounts, payment processing solutions, Credit Card Processing Services',
                               description = 'Explore the options in accepting card payments for your business. Come find the most cost-effective card payment processors with our reviews.')
