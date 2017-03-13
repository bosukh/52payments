from google.appengine.ext import ndb

class UserModel(ndb.Model):
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

    def __eq__(self, other):
        return self.user_id == other.user_id

    def __ne__(self, other):
        return not self.__eq__(self, other)

    @property
    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.user_id

    @property
    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return True #self.authenticated

    @property
    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
