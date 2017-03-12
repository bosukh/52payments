from google.appengine.ext import ndb

from .Company import CompanyModel
from .User import UserModel

class ReviewModel(ndb.Model):
    rating = ndb.IntegerProperty(required=True, indexed=True)
    title = ndb.StringProperty(required=True, indexed=True)
    content = ndb.TextProperty(required=True, indexed=False)
    approved = ndb.BooleanProperty(indexed=True)
    user = ndb.KeyProperty(UserModel, indexed=True)
    company = ndb.KeyProperty(CompanyModel, indexed=True)
    created = ndb.DateTimeProperty(auto_now_add = True, indexed=True)
    last_modified = ndb.DateTimeProperty(auto_now = True, indexed=True)

    def __eq__(self, other):
        return (self.title == other.title and \
                self.content == other.content)

    def __ne__(self, other):
        return not self.__eq__(self, other)

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
