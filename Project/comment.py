import cgi
import datetime
import urllib
import webapp2
import datastore
import config

from google.appengine.ext import db
from google.appengine.api import users

class RequestHandler(webapp2.RequestHandler):
	def get(self, article_id):
		template = config.templates.get_template(config.comments_page)
		article = datastore.get_article(article_id)

		# comment query
		comment_list = datastore.get_comments(article_id)

		# comment submission form
		self.response.write(template.render(
			{
				"article_name": article.text,
				"comments": comment_list, 
				"user": users.get_current_user()
			}))

	def post(self, article_id):
		#user login check
		user = users.get_current_user()
		comment_text = self.request.get('comment_text')

		if not user:
			self.redirect(users.create_login_url(self.request.uri))
                else:
			datastore.post_comment(article_id,
										users.get_current_user().nickname(),
										cgi.escape(comment_text))
			self.redirect('/comment/%s'% (article_id))
