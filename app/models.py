from google.appengine.ext import db

class Company(db.Model):
    title = db.StringProperty(required = True)
    company_profile_name = db.StringProperty(required = True)
    logo_file = db.BlobProperty(required = True)
    verified = db.BooleanProperty(default=False)
    summary = db.TextProperty(required = True)
    full_description = db.TextProperty(required = True)
    year_founded = db.FloatProperty()
    provided_srvs = db.StringListProperty(required=True)
    complementary_srvs = db.StringListProperty()
    equipment = db.StringListProperty()
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    num_ratings = db.IntegerProperty(default = 0, required=False)
    avg_rating = db.FloatProperty(default = 0.0, required=False)

class User(db.Model):
    name = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

class Review(db.Model):
    rating = db.FloatProperty(required=True)
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    user = db.ReferenceProperty(User)
    company = db.ReferenceProperty(Company)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def put_review(self):
        rating = self.rating
        self.put()
        company = self.company
        company.num_ratings += 1
        company.avg_rating = ((company.avg_rating * (company.num_ratings-1)) + rating) / company.num_ratings
        company.put()
