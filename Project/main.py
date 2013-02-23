import webapp2
import datastore
import config
import vote
import articles
import comment
import login
from google.appengine.ext import db
from google.appengine.api import users


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = config.templates.get_template(config.main_page)
        articles = datastore.get_articles()

        self.response.write(template.render(
            {
                "title": config.main_title, 
                "articles": articles, 
                "user": users.get_current_user()
            }))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', login.LoginPage),
    ('/logout', login.LogoutPage),
    ('/vote/(.*)', vote.RequestHandler),
    ('/article', articles.PostPage),
    ('/comment/(.*)', comment.RequestHandler)
    ], 
    debug=True)
