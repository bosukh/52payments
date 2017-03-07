from google.appengine.ext import ndb
from datetime import datetime
from functools import wraps
from flask_login import current_user
from uuid import uuid1
import logging
from .sticky_notes import add_notes

class TempCode(ndb.Model):
    code = ndb.StringProperty(required=True, indexed=True)
    value = ndb.StringProperty(required=True, indexed=False)
    created = ndb.DateTimeProperty(auto_now_add = True, indexed=False)

    @classmethod
    def gen_code(self):
        code = uuid1().get_hex()
        temp_code = TempCode(code=code, value=current_user.user_id)
        temp_code.put()
        return code

    @classmethod
    def verify_code(self, code, time = 0, delete=True):
        def time_diff(a, time):
            if time > 0:
                res = datetime.now() - a
                return res.seconds <= time
            return True
        temp_code = self.load_code(code)
        if temp_code:
            value = temp_code.value
            valid = time_diff(temp_code.created, time)
            if delete:
                temp_code.key.delete()
            if value and valid:
                return value
            else:
                return False
        return False

    @classmethod
    def load_code(self, code):
        query = self.gql("WHERE code = '%s'"%str(code))
        return query.get()

class Company(ndb.Model):
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

    @classmethod
    def load_company(self, company_profile_name):
        return self.make_query("WHERE company_profile_name = '%s'"%str(company_profile_name))()[0]


    @classmethod
    def make_query(self, query):
        '''
        returns a function.
        '''
        @wraps(self.gql(query).fetch)
        def decorated_function():
           return add_notes(self.gql(query).fetch())
        return decorated_function

class User(ndb.Model):
    user_id = ndb.StringProperty(required=True, indexed=True)
    first_name = ndb.StringProperty(required=True, indexed=False)
    last_name = ndb.StringProperty(required=True, indexed=False)
    company_name = ndb.StringProperty(required=False, indexed=False)
    email = ndb.StringProperty(required=True, indexed=True)
    email_verified = ndb.BooleanProperty(default=False, indexed=True)
    phone = ndb.StringProperty(required=False, indexed=False)
    phone_verified = ndb.BooleanProperty(default=False, indexed=True)
    password = ndb.StringProperty(default='', required=False, indexed=False)
    authenticated = ndb.BooleanProperty(default=False, indexed=False)
    company_admin = ndb.StringProperty(default= '', required=False, indexed=True)
    created = ndb.DateTimeProperty(auto_now_add = True, indexed=False)
    last_modified = ndb.DateTimeProperty(auto_now = True, indexed=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.user_id

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

class Review(ndb.Model):
    rating = ndb.IntegerProperty(required=True, indexed=True)
    title = ndb.StringProperty(required=True, indexed=True)
    content = ndb.TextProperty(required=True, indexed=False)
    approved = ndb.BooleanProperty(indexed=True)
    user = ndb.KeyProperty(User, indexed=True)
    company = ndb.KeyProperty(Company, indexed=True)
    created = ndb.DateTimeProperty(auto_now_add = True, indexed=True)
    last_modified = ndb.DateTimeProperty(auto_now = True, indexed=True)


    @classmethod
    def reviews_for_display(self, reviews):
        reviews = [review.to_dict() for review in reviews]
        for review in reviews:
            user = review['user'].get()
            review['user_name'] = user.first_name +" " + user.last_name[0].upper() + '.'
            review['created'] = review['created'].strftime('%b %d, %Y')
        return reviews

    def approve(self):
        self.approved = True
        rating = self.rating
        self.put()
        company = self.company.get()
        company.num_ratings += 1
        company.avg_rating = ((company.avg_rating * (company.num_ratings-1)) + rating) / company.num_ratings
        company.rounded_rating = int(round(company.avg_rating))
        company.put()
        return None
