#User Module
#uses the GAE users library for our accounts module

from google.appengine.api import users
from google.appengine.ext import webapp

class LoginPage(webapp.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			self.redirect('/')
		else:
			self.redirect(users.create_login_url("/"))

class LogoutPage(webapp.RequestHandler):
    def get(self):
        self.redirect(users.create_logout_url("/"))


