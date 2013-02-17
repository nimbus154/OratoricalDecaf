# vote.py
# Handles server-side logic for voting
# by Chad Wyszynski (chad.wyszynski@csu.fullerton.edu)
import webapp2
from google.appengine.api import users
import datastore
import simplejson as json
import logging

class RequestHandler(webapp2.RequestHandler):

    # valid vote types
    vote_types = {"up": 1, "down": -1}

    # Handles POST vote/{article_id}
    # returns: success - 200, update total votes for that article as JSON
    #          failure - error code with a short description of error in body
    def post(self, article_id):
        user = users.get_current_user()

        if(user):
            vote = self.extract_vote(self.request.body)
            if(self.is_valid_vote(vote)):
                votes = datastore.vote_article(user.email, 
                                                           article_id, 
                                        RequestHandler.vote_types[vote["vote"]])
                self.response.headers["Content-Type"] = "application/json"
                self.response.write(json.dumps({"article": article_id, 
                                                "votes": votes}))
            else:
                logging.debug(vote)
                print(vote)
                self.error(400) # bad request, no vote needs to be up or down
                self.response.write('Request must be {"vote": "up/down"}')
        else:
            self.error(401) # user must be logged in to vote
            self.response.write('You must be logged in to vote')

    # Checks if request_vote is a valid vote request
    # request_vote - vote to check
    # returns: true if valid request
    def is_valid_vote(self, request_vote):
        return "vote" in request_vote and \
                request_vote["vote"] in RequestHandler.vote_types

    # Extracts the "vote" request from the request body
    # returns: dictionary representing json request; empty dictionary if
    # unsuccessful
    def extract_vote(self, request_body):
            try:
                return json.loads(self.request.body)
            except json.JSONDecodeError: # unable to parse json
                return {"no": "deserialize"}

