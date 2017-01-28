from google.appengine.ext import ndb
from datetime import datetime

class TempCode(ndb.Model):
    code = ndb.StringProperty(required=True, indexed=True)
    value = ndb.StringProperty(required=True, indexed=False)
    created = ndb.DateTimeProperty(auto_now_add = True, indexed=False)

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
    company_profile_name = ndb.StringProperty(required = True, indexed=True)
    logo_file = ndb.BlobProperty(required = True, indexed=False)
    website = ndb.StringProperty(required = True, indexed=False)
    phones = ndb.StringProperty(repeated=True, indexed=False)
    verified = ndb.BooleanProperty(default=False, indexed=True)
    summary = ndb.TextProperty(required = True, indexed=False)
    full_description = ndb.TextProperty(required = True, indexed=False)
    year_founded = ndb.IntegerProperty(indexed=False)
    provided_srvs = ndb.StringProperty(repeated=True, indexed=True)
    complementary_srvs = ndb.StringProperty(repeated=True, indexed=True)
    equipment = ndb.StringProperty(repeated=True, indexed=True)
    pricing_method = ndb.StringProperty(repeated=True, indexed=True)
    pricing_range = ndb.FloatProperty(repeated=True, indexed=True)
    rate_range = ndb.FloatProperty(repeated=True, indexed=True)
    per_transaction_range = ndb.FloatProperty(repeated=True, indexed=True)
    num_ratings = ndb.IntegerProperty(default = 0, required=False, indexed=True)
    avg_rating = ndb.FloatProperty(default = 0.0, required=False, indexed=True)
    rounded_rating = ndb.IntegerProperty(default = 0, required=False, indexed=True)
    landing_page = ndb.StringProperty(required = False, indexed=False)
    featured = ndb.BooleanProperty(default=False, indexed=True)
    created = ndb.DateTimeProperty(auto_now_add = True, indexed=False)
    last_modified = ndb.DateTimeProperty(auto_now = True, indexed=False)

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

    def approve(self):
        self.approved = True
        rating = self.rating
        self.put()
        company = self.company.get()
        company.num_ratings += 1
        company.avg_rating = ((company.avg_rating * (company.num_ratings-1)) + rating) / company.num_ratings
        company.rounded_rating = int(round(company.avg_rating))
        company.put()
