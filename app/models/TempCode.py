from google.appengine.ext import ndb

from uuid import uuid1
from datetime import datetime
from flask_login import current_user

class TempCodeModel(ndb.Model):
    code = ndb.StringProperty(required=True, indexed=True)
    value = ndb.StringProperty(required=True, indexed=False)
    created = ndb.DateTimeProperty(auto_now_add = True, indexed=False)

    @classmethod
    def gen_code(self, value = None):
        code = uuid1().get_hex()
        temp_code = TempCodeModel(code=code, value=value or current_user.user_id)
        temp_code.put()
        return code

    @classmethod
    def verify_code(self, code, time = 0, delete=True):
        def time_diff(a, time):
            if time > 0:
                return (datetime.now() - a).seconds <= time
            return True
        temp_code = self.load_code(code)
        if temp_code:
            if delete:
                temp_code.key.delete()
            if temp_code.value and time_diff(temp_code.created, time):
                return temp_code.value
        return False

    @classmethod
    def load_code(self, code):
        query = self.gql("WHERE code = '%s'"%str(code))
        return query.get()
