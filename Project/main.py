import webapp2
import datastore
import config
import vote
import articles
import comment
from google.appengine.ext import db
from google.appengine.api import users


class MockUser():
    def __init__(self):
        self.nickname = "Bob"

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = config.templates.get_template(config.main_page)
        articles = datastore.get_articles()

        self.response.write(template.render(title=config.main_title, 
                                            data=articles, 
                                            user=MockUser()))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/vote/(.*)', vote.RequestHandler),
    ('/article', articles.PostPage),
    ('/comment/(.*)', comment.RequestHandler)
    ], 
    debug=True)
