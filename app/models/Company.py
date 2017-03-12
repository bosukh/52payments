from google.appengine.ext import ndb

from functools import wraps
from ..sticky_notes import add_notes

class CompanyModel(ndb.Model):
    title = ndb.StringProperty(required = True, indexed=True)
    updated = ndb.StringProperty(required = True, indexed=True)
    share = ndb.IntegerProperty(indexed=True)
    location = ndb.StringProperty(required = False, indexed=False)
    company_profile_name = ndb.StringProperty(required = True, indexed=True)
    logo_file = ndb.BlobProperty(required = False, indexed=False)
    website = ndb.StringProperty(required = True, indexed=False)
    phones = ndb.StringProperty(repeated=True, indexed=False)
    verified = ndb.BooleanProperty(default=False, indexed=True)
    highlights = ndb.StringProperty(repeated=True, indexed=False)
    full_description = ndb.TextProperty(required = True, indexed=False)
    promotion = ndb.StringProperty(required = False, indexed=False)
    meta_description = ndb.StringProperty(required = True, indexed=False)
    pricing_table = ndb.TextProperty(required = True, indexed=False)
    year_founded = ndb.IntegerProperty(indexed=False)
    provided_srvs = ndb.StringProperty(repeated=True, indexed=True)
    complementary_srvs = ndb.StringProperty(repeated=True, indexed=True)
    equipment = ndb.StringProperty(repeated=True, indexed=True)
    pricing_method = ndb.StringProperty(repeated=True, indexed=True)
    num_ratings = ndb.IntegerProperty(default = 0, required=False, indexed=True)
    avg_rating = ndb.FloatProperty(default = 0.0, required=False, indexed=True)
    rounded_rating = ndb.IntegerProperty(default = 0, required=False, indexed=True)
    landing_page = ndb.StringProperty(required = False, indexed=False)
    featured = ndb.BooleanProperty(default=False, indexed=True)
    created = ndb.DateTimeProperty(auto_now_add = True, indexed=False)
    last_modified = ndb.DateTimeProperty(auto_now = True, indexed=False)

    def __eq__(self, other):
        return self.company_profile_name == other.company_profile_name

    def __ne__(self, other):
        return not self.__eq__(self, other)

    @classmethod
    def load_company(self, company_profile_name, raw = False):
        '''
        Raw = False, transform data for templates
        company_profile_name is supposed to be unique.
        '''
        if raw:
            # can be get(), but just wanted to be consistent with make_query()
            res = self.gql("WHERE company_profile_name = '%s'"%str(company_profile_name)).fetch()
        else:
            res = self.make_query("WHERE company_profile_name = '%s'"%str(company_profile_name))()
        if res:
            return res[0]
        return None

    @classmethod
    def make_query(self, query):
        '''
        returns a function.
        '''
        @wraps(self.gql(query).fetch)
        def decorated_function():
           return add_notes(self.gql(query).fetch())
        return decorated_function
