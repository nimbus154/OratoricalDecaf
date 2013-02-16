# vote.py
# Handles server-side logic for voting
# by Chad Wyszynski (chad.wyszynski@csu.fullerton.edu)
import webapp2
from google.appengine.api import users
import datastore

class MockUser():
    def __init__(self, name):
        self.nickname = name

class RequestHandler(webapp2.RequestHandler):

# Handles POST vote/{article_id}
# returns: success - 200, update total votes for that article as JSON
#          failure - error code with a short description of error in body
    def post(self, article_id):
        user = MockUser("zero_cool") # users.get_current_user()
        if(user):
            vote_article(user.nickname, article_id, vote)
            self.response.headers["Content-Type"] = "application/json"
            self.response.write('{ "votes": %d }' % votes)
        else:
            self.error(401) # user must be logged in to vote
