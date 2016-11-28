from google.appengine.ext import ndb

class Company(ndb.Model):
    title = ndb.StringProperty(required = True)
    company_profile_name = ndb.StringProperty(required = True)
    logo_file = ndb.BlobProperty(required = True)
    verified = ndb.BooleanProperty(default=False)
    summary = ndb.TextProperty(required = True)
    full_description = ndb.TextProperty(required = True)
    year_founded = ndb.IntegerProperty()
    provided_srvs = ndb.StringProperty(repeated=True)
    complementary_srvs = ndb.StringProperty(repeated=True)
    equipment = ndb.StringProperty(repeated=True)
    pricing_method = ndb.StringProperty(repeated=True)
    pricing_range = ndb.FloatProperty(repeated=True)
    created = ndb.DateTimeProperty(auto_now_add = True)
    last_modified = ndb.DateTimeProperty(auto_now = True)
    num_ratings = ndb.IntegerProperty(default = 0, required=False)
    avg_rating = ndb.FloatProperty(default = 0.0, required=False)
    rounded_rating = ndb.IntegerProperty(default = 0, required=False)
    featured = ndb.BooleanProperty(default=False)

class User(ndb.Model):
    user_id = ndb.StringProperty(required=True)
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    phone = ndb.StringProperty(required=False)
    password = ndb.StringProperty(required=False)
    authenticated = ndb.BooleanProperty(default=False)
    company_admin = ndb.StringProperty(required=False)
    created = ndb.DateTimeProperty(auto_now_add = True)
    last_modified = ndb.DateTimeProperty(auto_now = True)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

class Review(ndb.Model):
    rating = ndb.IntegerProperty(required=True)
    title = ndb.StringProperty(required=True)
    content = ndb.TextProperty(required=True)
    approved = ndb.BooleanProperty(default=False)
    user = ndb.KeyProperty(User)
    company = ndb.KeyProperty(Company)
    created = ndb.DateTimeProperty(auto_now_add = True)
    last_modified = ndb.DateTimeProperty(auto_now = True)

    def approve(self):
        self.approved = True
        rating = self.rating
        self.put()
        company = self.company.get()
        company.num_ratings += 1
        company.avg_rating = ((company.avg_rating * (company.num_ratings-1)) + rating) / company.num_ratings
        company.rounded_rating = int(round(company.avg_rating))
        company.put()
