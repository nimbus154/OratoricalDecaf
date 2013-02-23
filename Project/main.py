import webapp2
import os
import datastore
import config
import vote
import articles
import comment
import jinja2
from google.appengine.ext import db
from google.appengine.api import users

# jinja2 file loading copied from 
# https://github.com/fRuiApps/cpfthw/blob/master/webapp2/views.py
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
j_env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = j_env.get_template(config.main_page)
	self.response.write('''
		<a href="/article">Post new article</a>
	''')
	articles = datastore.Get_Articles()
        self.response.write(template.render(title=config.main_title,data = articles))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/vote/(.*)', vote.RequestHandler),
    ('/article', articles.PostPage),
    ('/comment/(.*)', comment.RequestHandler)
    ], 
    debug=True)
